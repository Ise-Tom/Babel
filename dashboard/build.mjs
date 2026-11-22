import { build as bundle } from 'esbuild';
import { createHash } from 'node:crypto';
import { readFile, mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
export function jsonForHtml(value) {
  return JSON.stringify(value).replaceAll('<', '\\u003c').replaceAll('\u2028', '\\u2028').replaceAll('\u2029', '\\u2029');
}
export function hash(value) { return `sha256-${createHash('sha256').update(value).digest('base64')}`; }
export function textForHtml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}
export function validateBundledInputs(inputs) {
  const paths = Object.keys(inputs);
  if (!paths.length || paths.some(path => !path.startsWith('src/') || !path.endsWith('.ts') || path.includes('\\') || path.split('/').some(part => part === '..' || part === 'node_modules'))) {
    throw new Error('Bundled runtime dependencies need a reviewed distribution notice policy');
  }
}
export async function htmlFor(data) {
  const result = await bundle({ absWorkingDir: root, entryPoints: ['src/main.ts'], bundle: true, minify: true, write: false, format: 'iife', target: 'es2022', metafile: true });
  validateBundledInputs(result.metafile.inputs);
  const script = result.outputFiles[0].text.replaceAll('</script', '<\\/script');
  // HTML parsing normalizes line endings before the browser checks the CSP hash.
  const css = (await readFile(resolve(root, 'src/style.css'), 'utf8')).replace(/\r\n?/g, '\n');
  const embedded = jsonForHtml(data);
  const csp = `default-src 'none'; script-src '${hash(script)}' '${hash(embedded)}'; style-src '${hash(css)}'; img-src 'none'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'`;
  const notices = await Promise.all([
    readFile(resolve(root, '../LICENSE'), 'utf8'),
    readFile(resolve(root, '../NOTICE'), 'utf8'),
    readFile(resolve(root, 'node_modules/esbuild/LICENSE.md'), 'utf8'),
  ]);
  const retained = `Babel project license and notice\n\n${notices[0]}\n${notices[1]}\nesbuild build-tool notice (not an assertion of runtime linkage)\n\n${notices[2]}`;
  const replacements = { CSP: csp, CSS: css, DATA: embedded, JS: script, NOTICES: textForHtml(retained) };
  return (await readFile(resolve(root, 'src/index.html'), 'utf8'))
    .replace(/__(CSP|CSS|DATA|JS|NOTICES)__/g, (_, key) => replacements[key]);
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const data = JSON.parse(await readFile(resolve(root, 'generated/data.json'), 'utf8'));
  const output = resolve(root, 'dist/index.html');
  await mkdir(dirname(output), { recursive: true });
  await writeFile(output, await htmlFor(data));
  console.log(`Built standalone dashboard: ${output}`);
}
