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
export async function htmlFor(data) {
  const result = await bundle({ absWorkingDir: root, entryPoints: ['src/main.ts'], bundle: true, minify: true, write: false, format: 'iife', target: 'es2022' });
  const script = result.outputFiles[0].text.replaceAll('</script', '<\\/script');
  const css = await readFile(resolve(root, 'src/style.css'), 'utf8');
  const embedded = jsonForHtml(data);
  const csp = `default-src 'none'; script-src '${hash(script)}' '${hash(embedded)}'; style-src '${hash(css)}'; img-src 'none'; connect-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'`;
  return (await readFile(resolve(root, 'src/index.html'), 'utf8'))
    .replace('__CSP__', csp).replace('__CSS__', () => css).replace('__DATA__', () => embedded).replace('__JS__', () => script);
}
if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const data = JSON.parse(await readFile(resolve(root, 'generated/data.json'), 'utf8'));
  const output = resolve(root, 'dist/index.html');
  await mkdir(dirname(output), { recursive: true });
  await writeFile(output, await htmlFor(data));
  console.log(`Built standalone dashboard: ${output}`);
}
