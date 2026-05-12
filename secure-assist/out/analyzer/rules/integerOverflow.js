"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findIntegerOverflow = findIntegerOverflow;
const utils_1 = require("../utils");
function findIntegerOverflow(context) {
    if (context.language !== "cpp")
        return [];
    const findings = [];
    const { code, filePath } = context;
    const lines = code.split("\n");
    let offset = 0;
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i];
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith("//")) {
            offset += line.length + 1;
            continue;
        }
        if (!isRiskyIntegerOverflowLine(trimmed)) {
            offset += line.length + 1;
            continue;
        }
        const arithmeticVars = extractArithmeticVars(trimmed);
        if (isProtectedByAnyNearbyIf(lines, i, arithmeticVars)) {
            offset += line.length + 1;
            continue;
        }
        findings.push((0, utils_1.createFinding)({
            cweId: "CWE-190",
            ruleId: "integer-overflow",
            vulnerability: "Integer Overflow",
            severity: "medium",
            message: "This arithmetic operation may overflow before being used for allocation, copying, or size calculation.",
            file: filePath,
            code,
            index: offset + Math.max(0, line.indexOf(trimmed)),
            evidence: trimmed,
        }));
        offset += line.length + 1;
    }
    return findings;
}
function isRiskyIntegerOverflowLine(line) {
    if (isConstantOnlyArithmetic(line))
        return false;
    return (/\bmalloc\s*\([^)]*(\+|\*)[^)]*\)/.test(line) ||
        /\brealloc\s*\([^,]+,\s*[^)]*(\+|\*)[^)]*\)/.test(line) ||
        /\bmemcpy\s*\([^,]+,\s*[^,]+,\s*[^)]*(\+|\*)[^)]*\)/.test(line) ||
        /\b(?:int|short|long|size_t|unsigned|unsigned\s+int|unsigned\s+long)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*[^;]*(\+|\*)[^;]*;/.test(line));
}
function isConstantOnlyArithmetic(line) {
    const match = line.match(/=\s*([^;]+);/);
    if (!match)
        return false;
    const expr = match[1].trim();
    return /^[\d\s+\-*/()]+$/.test(expr);
}
function extractArithmeticVars(line) {
    const expr = extractRiskyArithmeticExpression(line);
    const vars = new Set();
    const parts = expr.match(/\b[a-zA-Z_][a-zA-Z0-9_]*\b\s*(?:\+|\*)\s*\b[a-zA-Z_][a-zA-Z0-9_]*\b/g);
    if (!parts)
        return [];
    for (const part of parts) {
        const names = part.match(/\b[a-zA-Z_][a-zA-Z0-9_]*\b/g) ?? [];
        for (const name of names) {
            if (!isIgnoredName(name)) {
                vars.add(name);
            }
        }
    }
    return Array.from(vars);
}
function extractRiskyArithmeticExpression(line) {
    const mallocMatch = line.match(/\bmalloc\s*\(([^)]*)\)/);
    if (mallocMatch)
        return mallocMatch[1];
    const reallocMatch = line.match(/\brealloc\s*\([^,]+,\s*([^)]*)\)/);
    if (reallocMatch)
        return reallocMatch[1];
    const memcpyMatch = line.match(/\bmemcpy\s*\([^,]+,\s*[^,]+,\s*([^)]*)\)/);
    if (memcpyMatch)
        return memcpyMatch[1];
    const assignmentMatch = line.match(/=\s*([^;]+);/);
    if (assignmentMatch)
        return assignmentMatch[1];
    return "";
}
function isProtectedByAnyNearbyIf(lines, currentLine, vars) {
    if (vars.length === 0)
        return false;
    const start = Math.max(0, currentLine - 10);
    for (let i = currentLine - 1; i >= start; i--) {
        const line = lines[i].trim();
        if (!line.startsWith("if")) {
            continue;
        }
        const conditionMatch = line.match(/\bif\s*\((.*)\)\s*\{?/);
        if (!conditionMatch) {
            continue;
        }
        const condition = conditionMatch[1];
        const allVarsChecked = vars.every((v) => variableHasBoundsCheck(condition, v));
        if (allVarsChecked) {
            return true;
        }
    }
    return false;
}
function variableHasBoundsCheck(condition, varName) {
    const escaped = escapeRegExp(varName);
    const cmp = `(<=|<|>=|>)`;
    const expr = `[\\w\\s/*+\\-]+`;
    return (new RegExp(`\\b${escaped}\\b\\s*${cmp}\\s*${expr}`).test(condition) ||
        new RegExp(`${expr}\\s*${cmp}\\s*\\b${escaped}\\b`).test(condition));
}
function isIgnoredName(name) {
    return [
        "malloc",
        "calloc",
        "realloc",
        "memcpy",
        "sizeof",
        "int",
        "short",
        "long",
        "size_t",
        "unsigned",
        "char",
        "void",
    ].includes(name);
}
function escapeRegExp(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
//# sourceMappingURL=integerOverflow.js.map