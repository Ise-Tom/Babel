import { ESLint } from 'eslint';
import ts from 'typescript';
import { readFile, readdir } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export async function lintTypeScript(code, filename, eslint = new ESLint()) {
  const source = ts.createSourceFile(filename, code, ts.ScriptTarget.Latest, true);
  const messages = [];
  function visit(node) {
    if (node.kind === ts.SyntaxKind.AnyKeyword) {
      const point = source.getLineAndCharacterOfPosition(node.getStart(source));
      messages.push({ ruleId: 'typescript/no-explicit-any', severity: 2,
        message: 'Use a concrete type or unknown instead of any.', line: point.line + 1, column: point.character + 1 });
    }
    ts.forEachChild(node, visit);
  }
  visit(source);
  const policy = { filePath: resolve(filename), messages, errorCount: messages.length,
    fatalErrorCount: 0, warningCount: 0, fixableErrorCount: 0, fixableWarningCount: 0 };
  if (source.isDeclarationFile) return [policy];
  const emitted = ts.transpileModule(code, { fileName: filename,
    compilerOptions: { target: ts.ScriptTarget.ES2022, module: ts.ModuleKind.ESNext } });
  // Erase types only: no bundling, minification or execution. DOM/eval rules see the runtime operations.
  const runtime = await eslint.lintText(emitted.outputText, { filePath: `${filename}.lint.js` });
  return [policy, ...runtime];
}

async function typedFiles(directory) {
  const result = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    const path = `${directory}/${entry.name}`;
    if (entry.isDirectory()) result.push(...await typedFiles(path));
    else if (entry.name.endsWith('.ts')) result.push(path);
  }
  return result;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const eslint = new ESLint();
  const results = await eslint.lintFiles(['*.mjs', 'tests/*.mjs']);
  for (const filename of [...await typedFiles('src'), ...await typedFiles('tests'), 'playwright.config.ts', 'build.d.mts']) {
    results.push(...await lintTypeScript(await readFile(filename, 'utf8'), filename, eslint));
  }
  const formatter = await eslint.loadFormatter('stylish');
  process.stdout.write(formatter.format(results));
  if (results.some(result => result.errorCount || result.warningCount)) process.exitCode = 1;
}
