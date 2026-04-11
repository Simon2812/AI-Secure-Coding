"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findPathTraversal = findPathTraversal;
const utils_1 = require("../utils");
function findPathTraversal(context) {
    const { language } = context;
    if (language === "python") {
        return findPythonPathTraversal(context);
    }
    if (language === "java") {
        return findJavaPathTraversal(context);
    }
    return [];
}
function findPythonPathTraversal(context) {
    const findings = [];
    const { code, filePath } = context;
    const lines = code.split("\n");
    const taintedVars = extractPythonTaintedVars(code);
    const constantStringVars = extractPythonConstantStringVars(code);
    let offset = 0;
    for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || trimmed.startsWith("#")) {
            offset += line.length + 1;
            continue;
        }
        const sinkMatches = [
            { regex: /\bopen\s*\((.*)\)/, sink: "open" },
            { regex: /\bos\.open\s*\((.*)\)/, sink: "os.open" },
            { regex: /\bsend_file\s*\((.*)\)/, sink: "send_file" },
            { regex: /\bsend_from_directory\s*\((.*)\)/, sink: "send_from_directory" },
            { regex: /\bshutil\.copy\s*\((.*)\)/, sink: "shutil.copy" },
            { regex: /\bshutil\.copyfile\s*\((.*)\)/, sink: "shutil.copyfile" },
            { regex: /\bshutil\.move\s*\((.*)\)/, sink: "shutil.move" },
            { regex: /\bzipfile\.ZipFile\s*\((.*)\)/, sink: "zipfile.ZipFile" },
            { regex: /\btarfile\.open\s*\((.*)\)/, sink: "tarfile.open" },
        ];
        for (const { regex } of sinkMatches) {
            const match = line.match(regex);
            if (!match || match.index === undefined) {
                continue;
            }
            const argsText = match[1]?.trim() ?? "";
            if (!argsText) {
                continue;
            }
            if (isClearlySafePythonExpression(argsText, constantStringVars)) {
                continue;
            }
            if (isPythonPathTraversalExpression(argsText, taintedVars, constantStringVars)) {
                findings.push((0, utils_1.createFinding)({
                    cweId: "CWE-22",
                    ruleId: "path-traversal",
                    vulnerability: "Path Traversal",
                    severity: "high",
                    message: "This file operation appears to use a user-controlled path without proper validation, which may allow directory traversal or access to unintended files.",
                    file: filePath,
                    code,
                    index: offset + match.index,
                    evidence: line.trim(),
                }));
            }
            break;
        }
        offset += line.length + 1;
    }
    return findings;
}
function findJavaPathTraversal(context) {
    const findings = [];
    const { code, filePath } = context;
    const taintedVars = extractJavaTaintedVars(code);
    const constantStringVars = extractJavaConstantStringVars(code);
    const sinkRegexes = [
        /\bnew\s+File\s*\(([\s\S]*?)\)/g,
        /\bnew\s+FileInputStream\s*\(([\s\S]*?)\)/g,
        /\bnew\s+FileOutputStream\s*\(([\s\S]*?)\)/g,
        /\bnew\s+FileReader\s*\(([\s\S]*?)\)/g,
        /\bnew\s+FileWriter\s*\(([\s\S]*?)\)/g,
        /\bnew\s+RandomAccessFile\s*\(([\s\S]*?)\)/g,
        /\bPaths\.get\s*\(([\s\S]*?)\)/g,
        /\bPath\.of\s*\(([\s\S]*?)\)/g,
        /\bFiles\.(?:readAllBytes|readString|lines|newInputStream|newBufferedReader|newBufferedWriter|writeString|newOutputStream|copy|move|delete|exists|isDirectory|isRegularFile)\s*\(([\s\S]*?)\)/g,
        /\bnew\s+ZipFile\s*\(([\s\S]*?)\)/g,
    ];
    for (const regex of sinkRegexes) {
        for (const match of code.matchAll(regex)) {
            if (match.index === undefined)
                continue;
            const argsText = extractRelevantArgs(match);
            if (!argsText)
                continue;
            if (isClearlySafeJavaExpression(argsText, constantStringVars)) {
                continue;
            }
            if (isJavaPathTraversalExpression(argsText, taintedVars, constantStringVars)) {
                findings.push((0, utils_1.createFinding)({
                    cweId: "CWE-22",
                    ruleId: "path-traversal",
                    vulnerability: "Path Traversal",
                    severity: "high",
                    message: "This file or path operation appears to use a user-controlled path without proper validation, which may allow directory traversal or access to unintended files.",
                    file: filePath,
                    code,
                    index: match.index,
                    evidence: match[0],
                }));
            }
        }
    }
    return findings;
}
function extractRelevantArgs(match) {
    const groups = match.slice(1).filter((value) => value !== undefined && value !== null);
    if (groups.length === 0) {
        return "";
    }
    return groups.map((part) => part.trim()).join(", ");
}
function extractPythonTaintedVars(code) {
    const tainted = new Set();
    let changed = true;
    const directPatterns = [
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*input\s*\(/gm,
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*sys\.argv\b/gm,
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*request\./gm,
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*request\.args\b/gm,
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*request\.form\b/gm,
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*request\.files\b/gm,
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*request\.values\b/gm,
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*request\.json\b/gm,
        /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*request\.get_json\s*\(/gm,
    ];
    for (const pattern of directPatterns) {
        for (const match of code.matchAll(pattern)) {
            tainted.add(match[1]);
        }
    }
    while (changed) {
        changed = false;
        const assignRegex = /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+)$/gm;
        for (const match of code.matchAll(assignRegex)) {
            const lhs = match[1];
            const rhs = match[2].trim();
            if (tainted.has(lhs)) {
                continue;
            }
            if (containsPythonDirectUserInput(rhs) || expressionUsesTaintedVar(rhs, tainted)) {
                tainted.add(lhs);
                changed = true;
            }
        }
    }
    return tainted;
}
function extractPythonConstantStringVars(code) {
    const constants = new Set();
    const literalAssignRegex = /^\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(["'][^"']*["'])\s*$/gm;
    for (const match of code.matchAll(literalAssignRegex)) {
        constants.add(match[1]);
    }
    return constants;
}
function extractJavaTaintedVars(code) {
    const tainted = new Set();
    let changed = true;
    const directPatterns = [
        /\bString\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*.*getParameter\s*\(/g,
        /\bString\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*.*getHeader\s*\(/g,
        /\bString\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*.*getQueryString\s*\(/g,
        /\bString\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*.*getPathInfo\s*\(/g,
        /\bString\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*.*nextLine\s*\(/g,
        /\bString\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*.*readLine\s*\(/g,
    ];
    for (const pattern of directPatterns) {
        for (const match of code.matchAll(pattern)) {
            tainted.add(match[1]);
        }
    }
    while (changed) {
        changed = false;
        const assignRegex = /^\s*(?:String|Path|File)?\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+);$/gm;
        for (const match of code.matchAll(assignRegex)) {
            const lhs = match[1];
            const rhs = match[2].trim();
            if (tainted.has(lhs)) {
                continue;
            }
            if (containsJavaDirectUserInput(rhs) || expressionUsesTaintedVar(rhs, tainted)) {
                tainted.add(lhs);
                changed = true;
            }
        }
    }
    return tainted;
}
function extractJavaConstantStringVars(code) {
    const constants = new Set();
    const literalAssignRegex = /\bString\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(["'][^"']*["'])\s*;/g;
    for (const match of code.matchAll(literalAssignRegex)) {
        constants.add(match[1]);
    }
    return constants;
}
function isPythonPathTraversalExpression(text, taintedVars, constantStringVars) {
    const expr = text.trim();
    if (!expr)
        return false;
    if (containsTraversalSequence(expr))
        return true;
    if (containsPythonDirectUserInput(expr))
        return true;
    if (isPlainIdentifier(expr) && taintedVars.has(expr))
        return true;
    if (isPlainIdentifier(expr) && constantStringVars.has(expr)) {
        return false;
    }
    if (expressionUsesTaintedVar(expr, taintedVars))
        return true;
    if (/os\.path\.join\s*\(/.test(expr)) {
        return !isPythonJoinSafe(expr, taintedVars, constantStringVars);
    }
    if (/(\+)|(\.format\s*\()|((^|[^a-zA-Z0-9_])f["'])/.test(expr)) {
        if (expressionUsesTaintedVar(expr, taintedVars) || containsPythonDirectUserInput(expr)) {
            return true;
        }
    }
    return false;
}
function isJavaPathTraversalExpression(text, taintedVars, constantStringVars) {
    const expr = text.trim();
    if (!expr)
        return false;
    if (containsTraversalSequence(expr))
        return true;
    if (containsJavaDirectUserInput(expr))
        return true;
    if (isPlainIdentifier(expr) && taintedVars.has(expr))
        return true;
    if (isPlainIdentifier(expr) && constantStringVars.has(expr)) {
        return false;
    }
    if (expressionUsesTaintedVar(expr, taintedVars))
        return true;
    if (/Paths\.get\s*\(/.test(expr) || /Path\.of\s*\(/.test(expr)) {
        return !isJavaPathFactorySafe(expr, taintedVars, constantStringVars);
    }
    if ((/\+/.test(expr) || /\.concat\s*\(/.test(expr)) && expressionUsesTaintedVar(expr, taintedVars)) {
        return true;
    }
    return false;
}
function isClearlySafePythonExpression(text, constantStringVars) {
    const expr = text.trim();
    if (!expr)
        return false;
    if (containsTraversalSequence(expr))
        return false;
    if (isOnlyStringLiteral(expr)) {
        return true;
    }
    if (isPlainIdentifier(expr) && constantStringVars.has(expr)) {
        return true;
    }
    if (isPythonJoinAllStringLiterals(expr)) {
        return true;
    }
    return false;
}
function isClearlySafeJavaExpression(text, constantStringVars) {
    const expr = text.trim();
    if (!expr)
        return false;
    if (containsTraversalSequence(expr))
        return false;
    if (isOnlyStringLiteral(expr)) {
        return true;
    }
    if (isPlainIdentifier(expr) && constantStringVars.has(expr)) {
        return true;
    }
    if (isJavaPathFactoryAllStringLiterals(expr)) {
        return true;
    }
    return false;
}
function containsTraversalSequence(text) {
    return text.includes("../") || text.includes("..\\");
}
function containsPythonDirectUserInput(text) {
    const patterns = [
        /\binput\s*\(/,
        /\bsys\.argv\b/,
        /\brequest\./,
        /\brequest\.args\b/,
        /\brequest\.form\b/,
        /\brequest\.files\b/,
        /\brequest\.values\b/,
        /\brequest\.json\b/,
        /\brequest\.get_json\s*\(/,
    ];
    return patterns.some((pattern) => pattern.test(text));
}
function containsJavaDirectUserInput(text) {
    const patterns = [
        /\brequest\./,
        /\breq\./,
        /\bgetParameter\s*\(/,
        /\bgetHeader\s*\(/,
        /\bgetQueryString\s*\(/,
        /\bgetPathInfo\s*\(/,
        /\bgetPart\s*\(/,
        /\bgetParts\s*\(/,
        /\bscanner\.next(Line)?\s*\(/i,
        /\breadLine\s*\(/,
        /\bargs\s*\[/,
    ];
    return patterns.some((pattern) => pattern.test(text));
}
function expressionUsesTaintedVar(text, taintedVars) {
    for (const varName of taintedVars) {
        const escaped = escapeRegExp(varName);
        const regex = new RegExp(`\\b${escaped}\\b`);
        if (regex.test(text)) {
            return true;
        }
    }
    return false;
}
function isPythonJoinSafe(text, taintedVars, constantStringVars) {
    const match = text.match(/^os\.path\.join\s*\((.*)\)$/);
    if (!match)
        return false;
    const args = splitTopLevelArgs(match[1]);
    if (args.length === 0)
        return false;
    return args.every((arg) => {
        const trimmed = arg.trim();
        return isOnlyStringLiteral(trimmed) || (isPlainIdentifier(trimmed) && constantStringVars.has(trimmed));
    });
}
function isJavaPathFactorySafe(text, taintedVars, constantStringVars) {
    const match = text.match(/^(?:Paths\.get|Path\.of)\s*\((.*)\)$/);
    if (!match)
        return false;
    const args = splitTopLevelArgs(match[1]);
    if (args.length === 0)
        return false;
    return args.every((arg) => {
        const trimmed = arg.trim();
        return isOnlyStringLiteral(trimmed) || (isPlainIdentifier(trimmed) && constantStringVars.has(trimmed));
    });
}
function isPythonJoinAllStringLiterals(text) {
    const match = text.match(/^os\.path\.join\s*\((.*)\)$/);
    if (!match)
        return false;
    const args = splitTopLevelArgs(match[1]);
    if (args.length === 0)
        return false;
    return args.every((arg) => isOnlyStringLiteral(arg.trim()));
}
function isJavaPathFactoryAllStringLiterals(text) {
    const match = text.match(/^(?:Paths\.get|Path\.of)\s*\((.*)\)$/);
    if (!match)
        return false;
    const args = splitTopLevelArgs(match[1]);
    if (args.length === 0)
        return false;
    return args.every((arg) => isOnlyStringLiteral(arg.trim()));
}
function splitTopLevelArgs(text) {
    const args = [];
    let current = "";
    let depth = 0;
    let quote = null;
    for (let i = 0; i < text.length; i++) {
        const ch = text[i];
        if (quote) {
            current += ch;
            if (ch === quote && text[i - 1] !== "\\") {
                quote = null;
            }
            continue;
        }
        if (ch === "'" || ch === '"') {
            quote = ch;
            current += ch;
            continue;
        }
        if (ch === "(") {
            depth++;
            current += ch;
            continue;
        }
        if (ch === ")") {
            depth--;
            current += ch;
            continue;
        }
        if (ch === "," && depth === 0) {
            args.push(current.trim());
            current = "";
            continue;
        }
        current += ch;
    }
    if (current.trim()) {
        args.push(current.trim());
    }
    return args;
}
function isOnlyStringLiteral(text) {
    const trimmed = text.trim();
    return /^"[^"]*"$/.test(trimmed) || /^'[^']*'$/.test(trimmed);
}
function isPlainIdentifier(text) {
    return /^[a-zA-Z_][a-zA-Z0-9_]*$/.test(text.trim());
}
function escapeRegExp(text) {
    return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
//# sourceMappingURL=pathTraversal.js.map