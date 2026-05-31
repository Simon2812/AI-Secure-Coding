import fs from "fs";
import { analyzeCode } from "./analyze";

/**
 * Analyzer runner.
 *
 * Responsibilities:
 * - read source code provided
 * - invoke analyzeCode()
 * - print findings as JSON
 *
 * Used by the Python evaluator.
 */

const filePath = process.argv[2];

if (!filePath) {
    console.error(
        "Usage: ts-node analyzer_runner.ts <filePath>"
    );

    process.exit(1);
}

const code = fs.readFileSync(
    filePath,
    "utf8"
);

const findings = analyzeCode(
    code,
    filePath
);

console.log(
    JSON.stringify(findings)
);
