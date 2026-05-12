"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findUseAfterFree = findUseAfterFree;
const utils_1 = require("../utils");
function findUseAfterFree(context) {
    if (context.language !== "cpp") {
        return [];
    }
    const findings = [];
    const { code, filePath } = context;
    const lines = code.split("\n");
    const freedVars = new Map();
    let offset = 0;
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith("//")) {
            offset += line.length + 1;
            continue;
        }
        const freeMatch = trimmed.match(/\bfree\s*\(\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\)\s*;/);
        if (freeMatch) {
            const varName = freeMatch[1];
            freedVars.set(varName, offset + line.indexOf("free"));
            offset += line.length + 1;
            continue;
        }
        for (const [varName] of freedVars) {
            if (isReassigned(trimmed, varName)) {
                freedVars.delete(varName);
                continue;
            }
            if (usesVariable(trimmed, varName)) {
                findings.push((0, utils_1.createFinding)({
                    cweId: "CWE-416",
                    ruleId: "use-after-free",
                    vulnerability: "Use After Free",
                    severity: "high",
                    message: "This code appears to use a pointer after it was freed. Accessing freed memory can cause crashes or security vulnerabilities.",
                    file: filePath,
                    code,
                    index: offset + line.indexOf(varName),
                    evidence: trimmed,
                }));
            }
        }
        offset += line.length + 1;
    }
    return findings;
}
function isReassigned(line, varName) {
    const escaped = escapeRegExp(varName);
    const assignmentRegex = new RegExp(`\\b${escaped}\\s*=`);
    const declarationAssignmentRegex = new RegExp(`\\b(?:char|int|float|double|void|long|short|struct\\s+\\w+)\\s*\\*?\\s*${escaped}\\s*=`);
    return assignmentRegex.test(line) || declarationAssignmentRegex.test(line);
}
function usesVariable(line, varName) {
    const escaped = escapeRegExp(varName);
    const patterns = [
        new RegExp(`\\b${escaped}\\b`),
        new RegExp(`\\*\\s*${escaped}\\b`),
        new RegExp(`\\b${escaped}\\s*\\[`),
        new RegExp(`\\b${escaped}\\s*->`),
    ];
    return patterns.some((pattern) => pattern.test(line));
}
function escapeRegExp(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
//# sourceMappingURL=useAfterFree.js.map