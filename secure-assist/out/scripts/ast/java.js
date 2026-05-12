"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.analyzeJava = analyzeJava;
const taint_1 = require("./taint");
const utils_1 = require("./utils");
const PATH_SINK_TYPES = new Set([
    "File", "FileInputStream", "FileOutputStream",
    "FileReader", "FileWriter", "RandomAccessFile", "ZipFile",
]);
const PATH_SINK_CALLS = new Set(["Paths.get", "Path.of"]);
const CMD_SINK_TYPES = new Set(["ProcessBuilder"]);
const CMD_SINK_CALLS = new Set(["Runtime.getRuntime().exec", "Runtime.exec"]);
const SQL_EXECUTE = new Set(["execute", "executeQuery", "executeUpdate"]);
const WEAK_HASH_ALGOS = /^"(MD5|SHA-?1)"$/i;
const WEAK_CIPHER_ALGOS = /^"DES(\/[^"]+)?"$/i;
function analyzeJava(code, filePath, tree) {
    const findings = [];
    const root = tree.rootNode;
    const taint = new taint_1.TaintTracker();
    seedJavaTaint(root, taint);
    taint.propagateAssignments(root, isJavaUserInputExpr);
    for (const node of (0, taint_1.walkAll)(root)) {
        // object_creation_expression: new File(...), new ProcessBuilder(...)
        if (node.type === "object_creation_expression") {
            const typeNode = node.childForFieldName("type");
            const argsNode = node.childForFieldName("arguments");
            const typeName = typeNode?.text ?? "";
            if (PATH_SINK_TYPES.has(typeName) && argsNode) {
                const args = getJavaArgs(argsNode);
                if (args.length > 0 && (taint.expressionIsTainted(args[0]) || isJavaUserInputExpr(args[0]))) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-22", ruleId: "ast-path-traversal",
                        vulnerability: "Path Traversal",
                        severity: "high",
                        message: `new ${typeName}() receives user-controlled path.`,
                        filePath, node: args[0], code,
                    }));
                }
            }
            if (CMD_SINK_TYPES.has(typeName) && argsNode) {
                const args = getJavaArgs(argsNode);
                if (args.some(a => taint.expressionIsTainted(a) || isJavaUserInputExpr(a))) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-78", ruleId: "ast-cmd-injection",
                        vulnerability: "OS Command Injection",
                        severity: "high",
                        message: `new ${typeName}() receives user-controlled input.`,
                        filePath, node, code,
                    }));
                }
            }
        }
        // method_invocation
        if (node.type === "method_invocation") {
            const methodName = node.childForFieldName("name")?.text ?? "";
            const argsNode = node.childForFieldName("arguments");
            const obj = node.childForFieldName("object");
            const fullName = obj ? `${obj.text}.${methodName}` : methodName;
            // Path sinks: Paths.get(), Path.of()
            if (PATH_SINK_CALLS.has(fullName) && argsNode) {
                const args = getJavaArgs(argsNode);
                if (args.some(a => taint.expressionIsTainted(a) || isJavaUserInputExpr(a))) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-22", ruleId: "ast-path-traversal",
                        vulnerability: "Path Traversal",
                        severity: "high",
                        message: `${fullName}() receives user-controlled path.`,
                        filePath, node, code,
                    }));
                }
            }
            // SQL sinks
            if (SQL_EXECUTE.has(methodName) && argsNode) {
                const args = getJavaArgs(argsNode);
                if (args.length > 0 && hasUnsafeSqlConstruction(args[0], taint)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-89", ruleId: "ast-sqli",
                        vulnerability: "SQL Injection",
                        severity: "high",
                        message: "SQL query constructed with user-controlled input.",
                        filePath, node: args[0], code,
                    }));
                }
            }
            // Weak crypto: MessageDigest.getInstance("MD5")
            if (methodName === "getInstance" && argsNode) {
                const args = getJavaArgs(argsNode);
                if (args.length > 0 && WEAK_HASH_ALGOS.test(args[0].text)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-327", ruleId: "ast-weak-hash",
                        vulnerability: "Use of Broken Cryptographic Algorithm",
                        severity: "medium",
                        message: `getInstance(${args[0].text}) uses a weak algorithm.`,
                        filePath, node, code,
                    }));
                }
                if (args.length > 0 && WEAK_CIPHER_ALGOS.test(args[0].text)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-327", ruleId: "ast-weak-cipher",
                        vulnerability: "Use of Broken Cryptographic Algorithm",
                        severity: "medium",
                        message: `getInstance(${args[0].text}) uses DES, an insecure cipher.`,
                        filePath, node, code,
                    }));
                }
            }
            // Command injection via Runtime.exec
            if ((methodName === "exec") && argsNode) {
                const args = getJavaArgs(argsNode);
                if (args.some(a => taint.expressionIsTainted(a) || isJavaUserInputExpr(a))) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-78", ruleId: "ast-cmd-injection",
                        vulnerability: "OS Command Injection",
                        severity: "high",
                        message: "Runtime.exec() receives user-controlled input.",
                        filePath, node, code,
                    }));
                }
            }
        }
    }
    findings.push(...findHardcodedCredentialsJava(root, filePath, code));
    return findings;
}
function seedJavaTaint(root, taint) {
    for (const node of (0, taint_1.walkAll)(root)) {
        // local_variable_declaration: Type name = expr;
        if (node.type === "local_variable_declaration") {
            const declarator = node.children.find(c => c.type === "variable_declarator");
            if (!declarator)
                continue;
            const nameNode = declarator.childForFieldName("name");
            const valueNode = declarator.childForFieldName("value");
            if (!nameNode || !valueNode)
                continue;
            if (isJavaUserInputExpr(valueNode)) {
                taint.add(nameNode.text);
            }
            continue;
        }
        // assignment_expression: name = expr (inside loops, if-blocks, etc.)
        if (node.type === "assignment_expression") {
            const left = node.childForFieldName("left");
            const right = node.childForFieldName("right");
            if (!left || !right || left.type !== "identifier")
                continue;
            if (isJavaUserInputExpr(right)) {
                taint.add(left.text);
            }
        }
    }
}
function isJavaUserInputExpr(node) {
    const text = node.text;
    if (/\bgetParameter\s*\(/.test(text))
        return true;
    if (/\bgetHeaders?\s*\(/.test(text))
        return true;
    if (/\bgetQueryString\s*\(/.test(text))
        return true;
    if (/\bgetPathInfo\s*\(/.test(text))
        return true;
    if (/\bgetParts?\s*\(/.test(text))
        return true;
    if (/\.getValue\s*\(/.test(text))
        return true;
    if (/\.nextElement\s*\(/.test(text))
        return true;
    if (/\.nextLine\s*\(/.test(text))
        return true;
    if (/\.readLine\s*\(/.test(text))
        return true;
    if (/\bargs\s*\[/.test(text))
        return true;
    return false;
}
function getJavaArgs(argsNode) {
    return argsNode.children.filter(c => c.type !== "," && c.type !== "(" && c.type !== ")");
}
function hasUnsafeSqlConstruction(node, taint) {
    const text = node.text.toLowerCase();
    if (!/\b(select|insert|update|delete)\b/.test(text))
        return false;
    if (node.type === "string_literal")
        return false;
    if (taint.expressionIsTainted(node))
        return true;
    if (node.type === "binary_expression" && node.text.includes("+"))
        return true;
    if (/String\.format\s*\(/.test(node.text))
        return true;
    return false;
}
// Sinks that indicate a string literal is used as a credential/key
const CRED_SINK_METHODS = new Set(["getConnection", "connect", "login", "authenticate"]);
const KEY_SINK_TYPES = new Set(["SecretKeySpec", "PBEKeySpec", "SecretKey"]);
const KEY_SINK_METHODS = new Set(["doFinal", "init", "encrypt", "decrypt", "sign", "verify"]);
function findHardcodedCredentialsJava(root, filePath, code) {
    const findings = [];
    const credVars = /^(password|passwd|pwd|secret|apiKey|api_key|token|authToken|accessToken|secretKey|clientSecret)$/i;
    // Track string literals assigned to any variable, then check if used in credential sinks
    const literalVars = new Map(); // varName → string literal node
    for (const node of (0, taint_1.walkAll)(root)) {
        // Collect all string-literal variable assignments
        if (node.type === "variable_declarator") {
            const nameNode = node.childForFieldName("name");
            const valueNode = node.childForFieldName("value");
            if (nameNode && valueNode && valueNode.type === "string_literal" && valueNode.text.length > 5) {
                literalVars.set(nameNode.text, valueNode);
            }
        }
        // Also catch assignment_expression: var = "literal"
        if (node.type === "assignment_expression") {
            const left = node.childForFieldName("left");
            const right = node.childForFieldName("right");
            if (left?.type === "identifier" && right?.type === "string_literal" && right.text.length > 5) {
                literalVars.set(left.text, right);
            }
        }
    }
    for (const node of (0, taint_1.walkAll)(root)) {
        // Pattern 1: variable name matches credential pattern → string literal value
        if (node.type === "variable_declarator") {
            const nameNode = node.childForFieldName("name");
            const valueNode = node.childForFieldName("value");
            if (!nameNode || !valueNode)
                continue;
            if (!credVars.test(nameNode.text))
                continue;
            if (valueNode.type === "string_literal" && valueNode.text.length > 5) {
                const cwe = /key|secret|token/i.test(nameNode.text) ? "CWE-321" : "CWE-259";
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: cwe, ruleId: "ast-hardcoded-cred",
                    vulnerability: cwe === "CWE-321" ? "Use of Hard-coded Cryptographic Key" : "Use of Hard-coded Password",
                    severity: "high",
                    message: `Hard-coded credential assigned to '${nameNode.text}'.`,
                    filePath, node: valueNode, code,
                }));
            }
        }
        // Pattern 2: string literal passed directly to credential/key sink methods
        if (node.type === "method_invocation") {
            const methodName = node.childForFieldName("name")?.text ?? "";
            const argsNode = node.childForFieldName("arguments");
            if (!argsNode)
                continue;
            const args = getJavaArgs(argsNode);
            if (CRED_SINK_METHODS.has(methodName)) {
                // Last arg of getConnection/connect is typically the password
                const lastArg = args[args.length - 1];
                if (lastArg && isHardcodedString(lastArg, literalVars)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-259", ruleId: "ast-hardcoded-cred",
                        vulnerability: "Use of Hard-coded Password",
                        severity: "high",
                        message: `Hard-coded password passed to ${methodName}().`,
                        filePath, node: lastArg, code,
                    }));
                }
            }
        }
        // Pattern 3: string literal used to construct SecretKeySpec / PBEKeySpec
        if (node.type === "object_creation_expression") {
            const typeNode = node.childForFieldName("type");
            const argsNode = node.childForFieldName("arguments");
            if (!typeNode || !argsNode)
                continue;
            if (!KEY_SINK_TYPES.has(typeNode.text))
                continue;
            const args = getJavaArgs(argsNode);
            // First arg is typically the key material
            if (args.length > 0 && isHardcodedKeyMaterial(args[0], literalVars)) {
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: "CWE-321", ruleId: "ast-hardcoded-cred",
                    vulnerability: "Use of Hard-coded Cryptographic Key",
                    severity: "high",
                    message: `Hard-coded key material passed to ${typeNode.text}.`,
                    filePath, node: args[0], code,
                }));
            }
        }
    }
    return findings;
}
function isHardcodedString(node, literalVars) {
    if (node.type === "string_literal")
        return node.text.length > 5;
    if (node.type === "identifier")
        return literalVars.has(node.text);
    return false;
}
function isHardcodedKeyMaterial(node, literalVars) {
    // getBytes() call on a string literal or literal variable
    if (node.type === "method_invocation") {
        const obj = node.childForFieldName("object");
        const method = node.childForFieldName("name")?.text;
        if (method === "getBytes" && obj)
            return isHardcodedString(obj, literalVars);
    }
    return isHardcodedString(node, literalVars);
}
//# sourceMappingURL=java.js.map