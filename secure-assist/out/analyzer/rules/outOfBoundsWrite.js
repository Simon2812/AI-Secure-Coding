"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findOutOfBoundsWrite = findOutOfBoundsWrite;
const utils_1 = require("../utils");
function findOutOfBoundsWrite(context) {
    if (context.language !== "cpp") {
        return [];
    }
    const findings = [];
    const { code, filePath } = context;
    const dangerousPatterns = [
        /\bgets\s*\(([^)]*)\)/g,
        /\bstrcpy\s*\(([^)]*)\)/g,
        /\bstrcat\s*\(([^)]*)\)/g,
        /\bsprintf\s*\(([^)]*)\)/g,
        /\bvsprintf\s*\(([^)]*)\)/g,
        /\bscanf\s*\(\s*"%s"\s*,\s*([^)]+)\)/g,
        /\bfscanf\s*\([^,]+,\s*"%s"\s*,\s*([^)]+)\)/g,
        /\bsscanf\s*\([^,]+,\s*"%s"\s*,\s*([^)]+)\)/g,
    ];
    for (const regex of dangerousPatterns) {
        for (const match of code.matchAll(regex)) {
            if (match.index === undefined)
                continue;
            findings.push((0, utils_1.createFinding)({
                cweId: "CWE-787",
                ruleId: "out-of-bounds-write",
                vulnerability: "Out-of-bounds Write",
                severity: "high",
                message: "This code uses a function that can write past the bounds of a buffer. Consider safer bounded alternatives such as fgets, snprintf, or explicit length checks.",
                file: filePath,
                code,
                index: match.index,
                evidence: match[0],
            }));
        }
    }
    return findings;
}
//# sourceMappingURL=outOfBoundsWrite.js.map