"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getLineAndColumn = getLineAndColumn;
exports.createFinding = createFinding;
exports.detectLanguage = detectLanguage;
function getLineAndColumn(text, index) {
    const before = text.slice(0, index);
    const lines = before.split("\n");
    return {
        line: lines.length,
        column: lines[lines.length - 1].length + 1,
    };
}
function createFinding(args) {
    const pos = getLineAndColumn(args.code, args.index);
    return {
        cweId: args.cweId,
        ruleId: args.ruleId,
        vulnerability: args.vulnerability,
        severity: args.severity,
        message: args.message,
        file: args.file,
        line: pos.line,
        column: pos.column,
        evidence: args.evidence,
    };
}
function detectLanguage(filePath) {
    const lower = filePath.toLowerCase();
    if (lower.endsWith(".c") || lower.endsWith(".cpp") || lower.endsWith(".cc") || lower.endsWith(".cxx") || lower.endsWith(".h") || lower.endsWith(".hpp")) {
        return "cpp";
    }
    if (lower.endsWith(".java")) {
        return "java";
    }
    if (lower.endsWith(".py")) {
        return "python";
    }
    return "unknown";
}
//# sourceMappingURL=utils.js.map