import js from "@eslint/js";

export default [
    js.configs.recommended,
    {
        files: ["**/*.js"],
        languageOptions: {
            ecmaVersion: 2020,
            sourceType: "module",
            globals: {
                console: "readonly",
                require: "readonly",
                process: "readonly",
                __dirname: "readonly",
                module: "readonly",
                fetch: "readonly",
                document: "readonly",
                window: "readonly",
                setTimeout: "readonly",
                clearTimeout: "readonly"
            }
        },
        rules: {
            "no-console": "off",
            "no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
        }
    }
];
