import js from '@eslint/js';
import tseslint from 'typescript-eslint';
import globals from 'globals';
import noUnsanitized from 'eslint-plugin-no-unsanitized';

export default [
  { ignores: ['dist/**', 'generated/**', 'node_modules/**', 'test-results/**', 'playwright-report/**'] },
  js.configs.recommended,
  ...tseslint.configs.recommended.map(config => ({ ...config, files: ['**/*.ts'] })),
  { languageOptions: { globals: { ...globals.node, ...globals.browser } },
    plugins: { 'no-unsanitized': noUnsanitized },
    rules: { 'no-eval': 'error', 'no-new-func': 'error', 'no-implied-eval': 'error',
      'no-script-url': 'error', 'no-unsanitized/method': 'error', 'no-unsanitized/property': 'error' } },
  { files: ['**/*.ts'], rules: { '@typescript-eslint/no-explicit-any': 'error' } }
];
