"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.analyzeCode = analyzeCode;
const hardcodedCredentials_1 = require("./rules/hardcodedCredentials");
// import { findWeakCrypto } from "./rules/weakCrypto";
// import { findCommandInjection } from "./rules/commandInjection";
function analyzeCode(code, filePath) {
    const findings = [];
    findings.push(...(0, hardcodedCredentials_1.findHardcodedCredentials)({ code, filePath }));
    //   findings.push(...findWeakCrypto({ code, filePath }));
    //   findings.push(...findCommandInjection({ code, filePath }));
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