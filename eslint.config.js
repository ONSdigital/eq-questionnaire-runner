import js from "@eslint/js";
import { importX } from "eslint-plugin-import-x";
import jsonPlugin from "eslint-plugin-json";
import n from "eslint-plugin-n";
import promise from "eslint-plugin-promise";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import playwright from "eslint-plugin-playwright";

export default [
  {
    ignores: [
      "node_modules/**",
      "htmlcov/**",
      "coverage/**",
      "dist/**",
      "src/index.html",
      "tests/functional/generated_pages/**"
    ]
  },
  {
    settings: {
      "import-x/resolver": {
        node: {
          extensions: [".js", ".cjs", ".mjs", ".ts", ".tsx", ".d.ts", ".json"]
        },
        typescript: {
          alwaysTryTypes: true
        }
      }
    }
  },
  js.configs.recommended,
  importX.flatConfigs.recommended,
  n.configs["flat/recommended-module"],
  promise.configs["flat/recommended"],
  {
    files: ["eslint.config.js"],
    rules: {
      "n/no-unpublished-import": 0
    }
  },
  {
    files: ["**/*.ts"],
    languageOptions: {
      parser: tsParser,
      ecmaVersion: "latest",
      sourceType: "module",
      parserOptions: {
        project: "./tsconfig.eslint.json"
      },
      globals: {
        process: "readonly"
      }
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
      playwright
    },
    rules: {
      ...(tsPlugin.configs.recommended.rules || {}),
      quotes: [
        2,
        "single",
        {
          avoidEscape: true,
          allowTemplateLiterals: true
        }
      ],
      semi: [2, "never"],
      "comma-dangle": [2, "never"],
      "space-before-function-paren": [2, "always"],
      "@typescript-eslint/no-unused-vars": 2,
      "@typescript-eslint/no-explicit-any": 0,
      "@typescript-eslint/no-useless-constructor": 2,
      "@typescript-eslint/explicit-function-return-type": 2,
      "@typescript-eslint/strict-boolean-expressions": 2,
      "@typescript-eslint/prefer-nullish-coalescing": 2,
      "@typescript-eslint/consistent-type-definitions": [2, "interface"],
      "@typescript-eslint/method-signature-style": [2, "property"],
      "@typescript-eslint/return-await": [2, "always"],
      "prefer-regex-literals": 2,
      "n/no-missing-import": 0,
      "n/no-unpublished-import": 0,
      "import-x/no-unresolved": [
        2,
        {
          ignore: ["generated_pages"]
        }
      ],
      "playwright/consistent-spacing-between-blocks": 2
    }
  },
  {
    files: ["**/*.json"],
    plugins: {
      json: jsonPlugin
    },
    processor: "json/json",
    rules: {
      "json/sort-keys": 0
    }
  }
];
