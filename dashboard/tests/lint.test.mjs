import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lintTypeScript } from '../lint.mjs';

test('typed text rendering and declaration files pass without executing application code', async () => {
  const results = await lintTypeScript('export function show(target: HTMLElement, text: string): void { target.textContent = text; }', 'src/fixture.ts');
  assert.equal(results.reduce((sum, result) => sum + result.errorCount, 0), 0);
  const declarations = await lintTypeScript('export declare function show(text: string): void;', 'build.d.mts');
  assert.equal(declarations[0].errorCount, 0);
});

test('type casts cannot hide DOM HTML sinks or eval from security lint', async () => {
  for (const [code, rule] of [
    ['export function show(target: HTMLElement, input: string) { (target as HTMLElement).innerHTML = input; }', 'no-unsanitized/property'],
    ['export function show(target: HTMLElement, input: string) { target.insertAdjacentHTML("beforeend", input); }', 'no-unsanitized/method'],
    ['export function show(input: string) { return eval(input); }', 'no-eval'],
  ]) {
    const results = await lintTypeScript(code, 'src/fixture.ts');
    assert.ok(results.flatMap(result => result.messages).some(message => message.ruleId === rule));
  }
});

test('explicit any is rejected before type erasure, including declarations', async () => {
  for (const filename of ['src/fixture.ts', 'build.d.mts']) {
    const results = await lintTypeScript('export declare const value: any;', filename);
    assert.ok(results.flatMap(result => result.messages).some(message => message.ruleId === 'typescript/no-explicit-any'));
  }
  const cast = await lintTypeScript('export function convert(value: unknown) { return value as any; }', 'src/fixture.ts');
  assert.ok(cast.flatMap(result => result.messages).some(message => message.ruleId === 'typescript/no-explicit-any'));
});
