"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.makeAstFinding = makeAstFinding;
function makeAstFinding(args) {
    return {
        cweId: args.cweId,
        ruleId: args.ruleId,
        vulnerability: args.vulnerability,
        severity: args.severity,
        message: args.message,
        file: args.filePath,
        line: args.node.startPosition.row + 1,
        column: args.node.startPosition.column + 1,
        evidence: args.node.text.slice(0, 120),
    };
}
//# sourceMappingURL=utils.js.map