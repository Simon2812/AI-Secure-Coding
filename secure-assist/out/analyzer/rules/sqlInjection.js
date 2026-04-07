"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findSqlInjection = findSqlInjection;
const utils_1 = require("../utils");
function findSqlInjection(context) {
    const { language } = context;
    if (language !== "python") {
        return [];
    }
    return findPythonSqlInjection(context);
}
function findPythonSqlInjection(context) {
    const findings = [];
    const { code, filePath } = context;
    const executeCallRegex = /\b[a-zA-Z_][a-zA-Z0-9_]*\.execute\s*\(([\s\S]*?)\)/g;
    for (const match of code.matchAll(executeCallRegex)) {
        if (match.index === undefined)
            continue;
        const fullCall = match[0];
        const argsText = match[1]?.trim() ?? "";
        if (isLikelyParameterizedExecute(argsText)) {
            continue;
        }
        if (isDangerousInlineSql(argsText)) {
            findings.push((0, utils_1.createFinding)({
                cweId: "CWE-89",
                ruleId: "python-sqli-inline",
                vulnerability: "SQL Injection",
                severity: "high",
                message: "Possible SQL injection: query appears to be built inline using unsafe string construction.",
                file: filePath,
                code,
                index: match.index,
                evidence: fullCall,
            }));
            continue;
        }
        const variableName = extractSingleVariable(argsText);
        if (variableName) {
            const assignment = findPreviousAssignment(code, variableName, match.index);
            if (assignment && isDangerousInlineSql(assignment.value)) {
                findings.push((0, utils_1.createFinding)({
                    cweId: "CWE-89",
                    ruleId: "python-sqli-variable",
                    vulnerability: "SQL Injection",
                    severity: "high",
                    message: `Possible SQL injection: SQL query variable "${variableName}" appears to be built unsafely before execution.`,
                    file: filePath,
                    code,
                    index: assignment.index,
                    evidence: assignment.fullMatch,
                }));
            }
        }
    }
    return findings;
}
function isLikelyParameterizedExecute(argsText) {
    const hasSecondArgument = topLevelCommaExists(argsText);
    if (!hasSecondArgument)
        return false;
    const firstArg = splitTopLevelArgs(argsText)[0] ?? "";
    return /(%s|\?)/.test(firstArg);
}
function isDangerousInlineSql(text) {
    const lower = text.toLowerCase();
    const looksLikeSql = /\b(select|insert|update|delete)\b/.test(lower);
    if (!looksLikeSql)
        return false;
    const isFString = /\bf["']/.test(text) || /\bf`/.test(text);
    const hasFormat = /\.format\s*\(/.test(text);
    const hasPercentFormatting = /["'][^"']*%[sd][^"']*["']\s*%/.test(text);
    const hasConcatenation = /["'][^"']*["']\s*\+/.test(text) || /\+\s*[a-zA-Z_][a-zA-Z0-9_]*/.test(text);
    return isFString || hasFormat || hasPercentFormatting || hasConcatenation;
}
function extractSingleVariable(argsText) {
    const trimmed = argsText.trim();
    if (/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(trimmed)) {
        return trimmed;
    }
    return null;
}
function findPreviousAssignment(code, variableName, beforeIndex) {
    const codeBefore = code.slice(0, beforeIndex);
    const escapedName = escapeRegex(variableName);
    const regex = new RegExp(`\\b${escapedName}\\s*=\\s*([^\\n]+)`, "g");
    let lastMatch = null;
    for (const match of codeBefore.matchAll(regex)) {
        lastMatch = match;
    }
    if (!lastMatch || lastMatch.index === undefined) {
        return null;
    }
    return {
        index: lastMatch.index,
        value: lastMatch[1],
        fullMatch: lastMatch[0],
    };
}
function splitTopLevelArgs(text) {
    const parts = [];
    let current = "";
    let depth = 0;
    let inSingle = false;
    let inDouble = false;
    for (let i = 0; i < text.length; i++) {
        const ch = text[i];
        const prev = i > 0 ? text[i - 1] : "";
        if (ch === "'" && !inDouble && prev !== "\\") {
            inSingle = !inSingle;
        }
        else if (ch === `"` && !inSingle && prev !== "\\") {
            inDouble = !inDouble;
        }
        if (!inSingle && !inDouble) {
            if (ch === "(" || ch === "[" || ch === "{")
                depth++;
            if (ch === ")" || ch === "]" || ch === "}")
                depth--;
            if (ch === "," && depth === 0) {
                parts.push(current.trim());
                current = "";
                continue;
            }
        }
        current += ch;
    }
    if (current.trim()) {
        parts.push(current.trim());
    }
    return parts;
}
function topLevelCommaExists(text) {
    return splitTopLevelArgs(text).length > 1;
}
function escapeRegex(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
//# sourceMappingURL=sqlInjection.js.map