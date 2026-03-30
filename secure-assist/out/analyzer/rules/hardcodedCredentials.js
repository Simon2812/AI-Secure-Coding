"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findHardcodedCredentials = findHardcodedCredentials;
const utils_1 = require("../utils");
function findHardcodedCredentials(context) {
    const findings = [];
    const { code, filePath } = context;
    const patterns = [
        {
            ruleId: "hardcoded-password",
            cweId: "CWE-798",
            vulnerability: "Use of Hard-coded Credentials",
            severity: "high",
            regex: /\b(password|passwd|pwd)\b\s*[:=]\s*["'`][^"'`\n]{3,}["'`]/gi,
            message: "Possible hard-coded password found in source code.",
        },
        {
            ruleId: "hardcoded-api-key",
            cweId: "CWE-798",
            vulnerability: "Use of Hard-coded Credentials",
            severity: "high",
            regex: /\b(api[_-]?key|apikey|client[_-]?secret|secret[_-]?key)\b\s*[:=]\s*["'`][^"'`\n]{6,}["'`]/gi,
            message: "Possible hard-coded API key or secret found in source code.",
        },
        {
            ruleId: "hardcoded-token",
            cweId: "CWE-798",
            vulnerability: "Use of Hard-coded Credentials",
            severity: "high",
            regex: /\b(token|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*["'`][^"'`\n]{6,}["'`]/gi,
            message: "Possible hard-coded authentication token found in source code.",
        },
    ];
    for (const pattern of patterns) {
        for (const match of code.matchAll(pattern.regex)) {
            if (match.index === undefined)
                continue;
            findings.push((0, utils_1.createFinding)({
                cweId: pattern.cweId,
                ruleId: pattern.ruleId,
                vulnerability: pattern.vulnerability,
                severity: pattern.severity,
                message: pattern.message,
                file: filePath,
                code,
                index: match.index,
                evidence: match[0],
            }));
        }
    }
    return findings;
}
//# sourceMappingURL=hardcodedCredentials.js.map