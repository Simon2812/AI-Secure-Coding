"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.analyzeCode = analyzeCode;
const utils_1 = require("./utils");
const hardcodedCredentials_1 = require("./rules/hardcodedCredentials");
const weakCrypto_1 = require("./rules/weakCrypto");
const commandInjection_1 = require("./rules/commandInjection");
function analyzeCode(code, filePath) {
    const context = {
        code,
        filePath,
        language: (0, utils_1.detectLanguage)(filePath),
    };
    const findings = [];
    findings.push(...(0, hardcodedCredentials_1.findHardcodedCredentials)(context));
    findings.push(...(0, weakCrypto_1.findWeakCrypto)(context));
    findings.push(...(0, commandInjection_1.findCommandInjection)(context));
    return sortFindings(findings);
}
function sortFindings(findings) {
    const severityOrder = {
        high: 0,
        medium: 1,
        low: 2,
    };
    return findings.sort((a, b) => {
        const sevDiff = severityOrder[a.severity] - severityOrder[b.severity];
        if (sevDiff !== 0)
            return sevDiff;
        if (a.line !== b.line)
            return a.line - b.line;
        return a.column - b.column;
    });
}
//# sourceMappingURL=analyze.js.map