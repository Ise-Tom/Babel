param([Parameter(Mandatory)][ValidateSet('inspect', 'create', 'delete')][string]$Action)
$ErrorActionPreference = 'Stop'
$item = [Console]::In.ReadToEnd() | ConvertFrom-Json
$run = [string]$item.run_id
if ($run -cnotmatch '^[a-f0-9]{32}$') { throw 'Invalid run ID' }
$prefix = "babel-$run-"
$kind = [string]$item.kind
$name = [string]$item.name
if ($kind -eq 'switch') {
    if ($name -cnotmatch "^babel-$run-(reference|babel)$") { throw 'Switch outside run scope' }
} elseif ($kind -eq 'vm') {
    if ($name -cnotmatch "^babel-$run-(reference-dc|reference-client|reference-probe|babel-dc|babel-client|babel-probe)$") { throw 'VM outside run scope' }
} elseif ($kind -eq 'disk') {
    $expected = "babel-lab-$run"
    $parent = Split-Path (Split-Path $name -Parent) -Leaf
    $leaf = Split-Path $name -Leaf
    if ($parent -cne $expected -or $leaf -cnotmatch '^(reference-dc|reference-client|reference-probe|babel-dc|babel-client|babel-probe)\.vhdx$') { throw 'Disk outside run scope' }
} else { throw 'Unknown resource kind' }

function Inspect {
    if ($kind -eq 'switch') {
        $resource = Get-VMSwitch -Name $name -ErrorAction SilentlyContinue
        if ($null -eq $resource) { return @{ exists = $false; owned = $false } }
        return @{ exists = $true; owned = ($resource.SwitchType -eq 'Private'); type = [string]$resource.SwitchType }
    }
    if ($kind -eq 'disk') {
        if (-not (Test-Path -LiteralPath $name -PathType Leaf)) { return @{ exists = $false; owned = $false } }
        $resource = Get-VHD -Path $name
        return @{ exists = $true; owned = ($resource.Path -ceq $name); type = [string]$resource.VhdType }
    }
    $resource = Get-VM -Name $name -ErrorAction SilentlyContinue
    if ($null -eq $resource) { return @{ exists = $false; owned = $false } }
    $adapters = @(Get-VMNetworkAdapter -VMName $name | ForEach-Object { $_.SwitchName })
    return @{ exists = $true; owned = ($resource.Notes -ceq "Babel isolated lab $run"); state = [string]$resource.State; switches = $adapters }
}

if ($Action -eq 'inspect') {
    Inspect | ConvertTo-Json -Compress -Depth 5
    exit 0
}
if ($Action -eq 'create') {
    if ((Inspect).exists) { throw 'Resource already exists' }
    if ($kind -eq 'switch') {
        New-VMSwitch -Name $name -SwitchType Private | Out-Null
    } elseif ($kind -eq 'disk') {
        New-VHD -Path $name -Dynamic -SizeBytes ([int64]$item.size_gib * 1GB) | Out-Null
    } else {
        if ($item.switch -cnotmatch "^babel-$run-(reference|babel)$") { throw 'VM switch outside run scope' }
        if ($item.disk -cnotmatch "[\\/]babel-lab-$run[\\/](reference-dc|reference-client|reference-probe|babel-dc|babel-client|babel-probe)\.vhdx$") { throw 'VM disk outside run scope' }
        if ($item.media_path -notmatch '\.iso$' -or -not (Test-Path -LiteralPath $item.media_path -PathType Leaf)) { throw 'Verified local ISO required' }
        if ((Get-FileHash -LiteralPath $item.media_path -Algorithm SHA256).Hash.ToLowerInvariant() -cne [string]$item.media_sha256) { throw 'Media changed before VM creation' }
        if ((Get-VMSwitch -Name $item.switch).SwitchType -ne 'Private') { throw 'Only a private switch is allowed' }
        New-VM -Name $name -Generation 2 -NoVHD -MemoryStartupBytes ([int64]$item.memory_mib * 1MB) -SwitchName $item.switch | Out-Null
        Set-VM -Name $name -Notes "Babel isolated lab $run" -ProcessorCount ([int]$item.cpus) -AutomaticStartAction Nothing -AutomaticStopAction ShutDown
        Add-VMHardDiskDrive -VMName $name -Path $item.disk
        $dvd = Add-VMDvdDrive -VMName $name -Path $item.media_path -Passthru
        Set-VMFirmware -VMName $name -FirstBootDevice $dvd
        if ($item.guest_id -match '(probe|babel-dc)$') { Set-VMFirmware -VMName $name -SecureBootTemplate 'MicrosoftUEFICertificateAuthority' }
        Start-VM -Name $name | Out-Null
    }
    @{ created = $true } | ConvertTo-Json -Compress
    exit 0
}
$observed = Inspect
if (-not $observed.exists) { @{ deleted = $false } | ConvertTo-Json -Compress; exit 0 }
if (-not $observed.owned) { throw 'Resource ownership mismatch' }
if ($kind -eq 'vm') {
    if ($observed.state -ne 'Off') { Stop-VM -Name $name -TurnOff -Force | Out-Null }
    Remove-VM -Name $name -Force | Out-Null
} elseif ($kind -eq 'disk') {
    $attached = @(Get-VM | Get-VMHardDiskDrive | Where-Object { $_.Path -ceq $name })
    if ($attached.Count -ne 0) { throw 'Disk is attached to a VM' }
    Remove-Item -LiteralPath $name -Force
} else {
    $attached = @(Get-VM | Get-VMNetworkAdapter | Where-Object { $_.SwitchName -ceq $name })
    if ($attached.Count -ne 0) { throw 'Switch has attached adapters' }
    Remove-VMSwitch -Name $name -Force | Out-Null
}
@{ deleted = $true } | ConvertTo-Json -Compress
