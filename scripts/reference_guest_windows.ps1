param(
    [Parameter(Mandatory)][string]$Config,
    [Parameter(Mandatory)][string]$Report
)
$ErrorActionPreference = 'Stop'
$cfg = Get-Content -LiteralPath $Config -Raw | ConvertFrom-Json
if ($cfg.role -notin @('windows_reference_dc', 'windows_client')) { throw 'Windows guest role required' }
if ($cfg.run_id -cnotmatch '^[a-f0-9]{32}$' -or $cfg.plan_sha256 -cnotmatch '^[a-f0-9]{64}$') { throw 'Invalid runner binding' }
if ($cfg.interface -notmatch '^[A-Za-z0-9 ._-]{1,64}$' -or $null -ne $cfg.default_gateway) { throw 'Unsafe interface or route' }
$scriptHash = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($scriptHash -cne [string]$cfg.script_sha256) { throw 'Guest script differs from prepared bundle' }
$stepNames = @('updates_verified','updates_installed','network_configured','dns_configured','time_configured','platform_observed','dns_probe','time_probe','egress_probe')
$steps = [ordered]@{}
foreach ($name in $stepNames) { $steps[$name] = 'pending' }
$record = [ordered]@{
    schema_version = 1
    run_id = [string]$cfg.run_id
    plan_sha256 = [string]$cfg.plan_sha256
    guest_id = [string]$cfg.guest_id
    vm = [string]$cfg.vm
    script_sha256 = $scriptHash
    status = 'incomplete'
    steps = $steps
    observed = [ordered]@{}
}
function Save-Report {
    $json = $record | ConvertTo-Json -Depth 12
    $temporary = "$Report.tmp"
    [IO.File]::WriteAllText($temporary, "$json`n", [Text.UTF8Encoding]::new($false))
    Move-Item -LiteralPath $temporary -Destination $Report -Force
}
Save-Report
$step = 'updates_verified'
try {
    $updates = @()
    foreach ($update in $cfg.updates) {
        if ($update.filename -cnotmatch '^update-[1-9][0-9]*\.(msu|cab)$') { throw 'Unsupported staged update' }
        $file = Join-Path (Split-Path $Config -Parent) $update.filename
        if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw 'Staged update missing' }
        if ((Get-Item -LiteralPath $file).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Staged update link refused' }
        if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash.ToLowerInvariant() -cne [string]$update.sha256) { throw 'Staged update digest changed' }
        $updates += $file
    }
    $record.steps[$step] = 'passed'; Save-Report

    $step = 'updates_installed'
    foreach ($file in $updates) {
        & dism.exe /Online /Add-Package "/PackagePath:$file" /Quiet /NoRestart | Out-Null
        if ($LASTEXITCODE -ne 0) { throw "DISM requires review or reboot (exit $LASTEXITCODE)" }
    }
    $record.observed['applied_update_sha256'] = @($cfg.updates | ForEach-Object { [string]$_.sha256 })
    $record.steps[$step] = 'passed'; Save-Report

    $step = 'network_configured'
    $adapter = @(Get-NetAdapter -Physical | Where-Object { $_.Status -eq 'Up' })
    if ($adapter.Count -ne 1 -or $adapter[0].Name -cne [string]$cfg.interface) { throw 'Exactly one planned private adapter required' }
    if (@(Get-NetRoute -AddressFamily IPv4 -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue).Count -ne 0) { throw 'Preexisting default route' }
    $address = @(Get-NetIPAddress -InterfaceAlias $cfg.interface -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike '169.254.*' })
    if ($address.Count -gt 1 -or ($address.Count -eq 1 -and ($address[0].IPAddress -cne [string]$cfg.address -or $address[0].PrefixLength -ne [int]$cfg.prefix_length))) { throw 'Unexpected interface address' }
    if ($address.Count -eq 0) { New-NetIPAddress -InterfaceAlias $cfg.interface -IPAddress $cfg.address -PrefixLength $cfg.prefix_length -AddressFamily IPv4 | Out-Null }
    $record.steps[$step] = 'passed'; Save-Report

    $step = 'dns_configured'
    Set-DnsClientServerAddress -InterfaceAlias $cfg.interface -ServerAddresses @($cfg.dns_server)
    Set-DnsClient -InterfaceAlias $cfg.interface -ConnectionSpecificSuffix $cfg.dns_suffix
    $record.steps[$step] = 'passed'; Save-Report

    $step = 'time_configured'
    if ($cfg.role -eq 'windows_reference_dc') {
        Set-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Services\W32Time\TimeProviders\NtpServer' -Name Enabled -Value 1
        & w32tm.exe /config /reliable:yes /update | Out-Null
    } else {
        & w32tm.exe /config "/manualpeerlist:$($cfg.time_server)" /syncfromflags:manual /update | Out-Null
    }
    if ($LASTEXITCODE -ne 0) { throw 'Windows Time configuration failed' }
    Restart-Service W32Time
    if ($cfg.role -ne 'windows_reference_dc') {
        & w32tm.exe /resync /force | Out-Null
        if ($LASTEXITCODE -ne 0) { throw 'Windows Time resync failed' }
    }
    $record.steps[$step] = 'passed'; Save-Report

    $step = 'platform_observed'
    $os = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    $build = "10.0.$($os.CurrentBuildNumber).$($os.UBR)"
    $packages = [ordered]@{}
    foreach ($property in $cfg.expected_packages.PSObject.Properties) {
        $pin = [string]$property.Value
        if ($pin -notmatch '^KB[0-9]+$') { throw 'Windows package pin must be a KB identifier' }
        $hotfix = Get-HotFix -Id $pin -ErrorAction SilentlyContinue
        if ($null -eq $hotfix) {
            $package = @(Get-WindowsPackage -Online | Where-Object { $_.PackageName -match $pin -and $_.PackageState -eq 'Installed' })
            if ($package.Count -eq 0) { throw "Pinned Windows update not installed: $pin" }
        }
        $packages[$property.Name] = $pin
    }
    $record.observed['build'] = $build
    $record.observed['edition'] = [string]$os.EditionID
    $record.observed['packages'] = $packages
    $record.steps[$step] = 'passed'; Save-Report

    $step = 'dns_probe'
    $suffix = [string]$cfg.dns_suffix
    $server = [string]$cfg.dns_server
    $a = @(Resolve-DnsName -Name "dc.$suffix" -Type A -Server $server -ErrorAction Stop | Where-Object { $_.Type -eq 'A' })
    $srv = @(Resolve-DnsName -Name "_ldap._tcp.$suffix" -Type SRV -Server $server -ErrorAction Stop | Where-Object { $_.Type -eq 'SRV' })
    $observedA = if ($a.Count) { [string]$a[0].IPAddress } else { '' }
    $observedSrv = if ($srv.Count) { ([string]$srv[0].NameTarget).TrimEnd('.') } else { '' }
    $client = [Net.Sockets.TcpClient]::new()
    try { $ldapOpen = $client.ConnectAsync($server, 389).Wait(3000) -and $client.Connected } finally { $client.Dispose() }
    $record.observed['probes'] = [ordered]@{
        dc_a = @{ expected = $server; observed = $observedA; status = $(if ($observedA -ceq $server) {'passed'} else {'failed'}) }
        ldap_srv = @{ expected = "dc.$suffix"; observed = $observedSrv; status = $(if ($observedSrv -ceq "dc.$suffix") {'passed'} else {'failed'}) }
        ldap_tcp = @{ expected = $true; observed = $ldapOpen; status = $(if ($ldapOpen) {'passed'} else {'failed'}) }
    }
    if (@($record.observed['probes'].Values | Where-Object { $_.status -ne 'passed' }).Count) { throw 'Discovery probe mismatch' }
    $record.steps[$step] = 'passed'; Save-Report

    $step = 'time_probe'
    $strip = (& w32tm.exe /stripchart "/computer:$($cfg.time_server)" /samples:1 /dataonly 2>&1) -join ' '
    if ($LASTEXITCODE -ne 0 -or $strip -notmatch '([-+]?[0-9]+[.,][0-9]+)s') { throw 'Windows Time offset unavailable' }
    $offset = [double]::Parse($Matches[1].Replace(',','.'), [Globalization.CultureInfo]::InvariantCulture) * 1000
    $record.observed['time_offset_ms'] = $offset
    if ([math]::Abs($offset) -gt 5000) { throw 'Clock offset exceeds five seconds' }
    $record.steps[$step] = 'passed'; Save-Report

    $step = 'egress_probe'
    $egress = [Net.Sockets.TcpClient]::new()
    try { $outbound = $egress.ConnectAsync('203.0.113.1', 443).Wait(3000) -and $egress.Connected } finally { $egress.Dispose() }
    $routes = @(Get-NetRoute -AddressFamily IPv4 -DestinationPrefix '0.0.0.0/0' -ErrorAction SilentlyContinue)
    $dns = @((Get-DnsClientServerAddress -InterfaceAlias $cfg.interface -AddressFamily IPv4).ServerAddresses)
    $effectiveIp = @(Get-NetIPAddress -InterfaceAlias $cfg.interface -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike '169.254.*' })
    $record.observed['address'] = if ($effectiveIp.Count -eq 1) { [string]$effectiveIp[0].IPAddress } else { '' }
    $record.observed['dns_servers'] = $dns
    $record.observed['dns_suffix'] = [string](Get-DnsClient -InterfaceAlias $cfg.interface).ConnectionSpecificSuffix
    $record.observed['default_routes'] = @($routes | ForEach-Object { $_.NextHop })
    $record.observed['denied_egress'] = -not $outbound
    if ($outbound -or $routes.Count -or $dns.Count -ne 1 -or $dns[0] -cne [string]$cfg.dns_server -or $record.observed['address'] -cne [string]$cfg.address) { throw 'Isolation probe failed' }
    $record.steps[$step] = 'passed'
    $record.status = 'complete'
    Save-Report
} catch {
    $record.steps[$step] = 'failed'
    $record.status = 'incomplete'
    Save-Report
    throw
}
