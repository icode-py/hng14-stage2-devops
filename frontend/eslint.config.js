const js = require("@eslint/js");

module.exports = [
    js.configs.recommended,
    {
        files: ["**/*.js"],
        languageOptions: {
            ecmaVersion: 2020,
            sourceType: "commonjs",
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