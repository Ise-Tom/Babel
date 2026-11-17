import js from '@eslint/js';
import globals from 'globals';
import noUnsanitized from 'eslint-plugin-no-unsanitized';

export default [
  { ignores: ['dist/**', 'generated/**', 'node_modules/**', 'test-results/**', 'playwright-report/**'] },
  js.configs.recommended,
  { languageOptions: { globals: { ...globals.node, ...globals.browser } },
    plugins: { 'no-unsanitized': noUnsanitized },
    rules: { 'no-eval': 'error', 'no-new-func': 'error', 'no-implied-eval': 'error',
      'no-script-url': 'error', 'no-unsanitized/method': 'error', 'no-unsanitized/property': 'error' } },
];
