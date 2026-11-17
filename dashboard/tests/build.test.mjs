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
