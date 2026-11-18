import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { htmlFor, jsonForHtml, hash } from '../build.mjs';

const model = JSON.parse(await readFile(new URL('../generated/data.json', import.meta.url), 'utf8'));
test('embedded data cannot terminate the JSON script element', () => {
  const payload = '</ScRiPt><script>globalThis.compromised=true</script>\u2028\u2029';
  const encoded = jsonForHtml({ payload });
  assert.ok(!encoded.includes('<'));
  assert.deepEqual(JSON.parse(encoded), { payload });
});
test('standalone builds are deterministic and CSP matches exact inline bytes', async () => {
  const first = await htmlFor(model);
  assert.equal(first, await htmlFor(model));
  for (const regex of [/<style>([\s\S]*?)<\/style>/g, /<script(?: [^>]*)?>([\s\S]*?)<\/script>/g]) {
    for (const match of first.matchAll(regex)) assert.ok(first.includes(hash(match[1])));
  }
  assert.ok(first.includes("connect-src 'none'"));
  assert.ok(first.includes("img-src 'none'"));
  assert.ok(first.includes('<meta name="referrer" content="no-referrer">'));
  assert.ok(!first.includes("'unsafe-inline'"));
  assert.ok(!first.includes('src="http'));
  assert.ok(!first.includes('href="http'));
});
test('hostile document text remains encoded in a complete build', async () => {
  const data = structuredClone(model);
  data.phases[0].title = '</script><img src=x onerror="globalThis.compromised=true">';
  const html = await htmlFor(data);
  assert.ok(!html.includes('<img src=x'));
  assert.ok(html.includes('\\u003c/script>'));
});
test('standalone distribution retains full project and build-tool notices inertly', async () => {
  const html = await htmlFor(model);
  const { textForHtml } = await import('../build.mjs');
  for (const url of [new URL('../../LICENSE', import.meta.url), new URL('../../NOTICE', import.meta.url), new URL('../node_modules/esbuild/LICENSE.md', import.meta.url)]) {
    assert.ok(html.includes(textForHtml(await readFile(url, 'utf8'))));
  }
  assert.ok(html.includes('<template id="license-notices"><pre>'));
  assert.equal(textForHtml('</template><script>&'), '&lt;/template&gt;&lt;script&gt;&amp;');
});
test('authored placeholder text cannot consume subsequent build replacements', async () => {
  const data = structuredClone(model);
  data.phases[0].title = '__JS__ __CSP__ __CSS__ __DATA__ __NOTICES__';
  const html = await htmlFor(data);
  const embedded = html.match(/<script id="dashboard-data" type="application\/json">([\s\S]*?)<\/script>/)?.[1];
  assert.ok(embedded);
  assert.deepEqual(JSON.parse(embedded), data);
  assert.ok(!html.includes('<script>__JS__</script>'));
});
test('new bundled runtime dependencies cannot silently omit their redistribution review', async () => {
  const { validateBundledInputs } = await import('../build.mjs');
  validateBundledInputs({ 'src/main.ts': {}, 'src/dom.ts': {} });
  for (const name of ['node_modules/runtime/index.ts', '../outside.ts', 'src/../outside.ts', 'src/node_modules/vendor/index.ts', 'src\\runtime.ts', 'src/unreviewed.js']) {
    assert.throws(() => validateBundledInputs({ [name]: {} }), /notice policy/);
  }
  assert.throws(() => validateBundledInputs({}), /notice policy/);
});
