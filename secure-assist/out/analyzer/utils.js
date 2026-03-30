"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getLineAndColumn = getLineAndColumn;
exports.createFinding = createFinding;
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
//# sourceMappingURL=utils.js.map