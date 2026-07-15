import js from "@eslint/js";
import { importX } from "eslint-plugin-import-x";
import jsonPlugin from "eslint-plugin-json";
import n from "eslint-plugin-n";
import promise from "eslint-plugin-promise";
import globals from "globals";

export default [
  {
    ignores: ["node_modules/**", "htmlcov/**", "coverage/**", "dist/**", "src/index.html", "tests/functional/generated_pages/**"],
  },
  js.configs.recommended,
  importX.flatConfigs.recommended,
  n.configs["flat/recommended-module"],
  promise.configs["flat/recommended"],
  {
    files: ["**/*.js", "**/*.cjs"],
    languageOptions: {
      ecmaVersion: 11,
      sourceType: "module",
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.mocha,
        $: "readonly",
        $$: "readonly",
        browser: "readonly",
        expect: "readonly",
      },
    },
    plugins: {
      "import-x": importX,
      json: jsonPlugin,
    },
    rules: {
      "no-loss-of-precision": 0,
      "no-nonoctal-decimal-escape": 0,
      "no-unsafe-optional-chaining": 0,
      "no-useless-backreference": 0,
      "consistent-return": 1,
      quotes: [
        2,
        "double",
        {
          avoidEscape: true,
          allowTemplateLiterals: true,
        },
      ],
      semi: [2, "always"],
      "space-before-function-paren": 0,
      indent: [
        2,
        2,
        {
          SwitchCase: 1,
        },
      ],
      "padded-blocks": [
        "error",
        {
          blocks: "never",
        },
      ],
      "comma-dangle": 0,
      "new-cap": 2,
      "no-alert": 1,
      "no-console": 2,
      "no-dupe-class-members": 0,
      "no-unused-expressions": 0,
      "no-var": 2,
      "n/no-extraneous-import": 0,
      "n/no-unpublished-import": 0,
      "prefer-arrow-callback": [
        2,
        {
          allowNamedFunctions: false,
        },
      ],
      "require-await": "error",
      "import-x/no-unresolved": [
        2,
        {
          ignore: ["generated_pages"],
        },
      ],
    },
  },
  {
    files: ["**/*.json"],
    plugins: {
      json: jsonPlugin,
    },
    processor: "json/json",
    rules: {
      "json/sort-keys": 0,
    },
  },
  {
    files: ["tests/functional/**/*.js"],
    rules: {
      // Functional specs import generated pages that are not present in MegaLinter CI runs.
      "n/no-missing-import": 0,
    },
  },
];
