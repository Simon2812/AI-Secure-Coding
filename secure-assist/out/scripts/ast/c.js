"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.analyzeC = analyzeC;
const taint_1 = require("./taint");
const utils_1 = require("./utils");
const OOB_WRITE_FUNCS = new Set(["gets", "strcpy", "strcat", "sprintf", "vsprintf"]);
const OVERFLOW_ALLOC_FUNCS = new Set(["malloc", "realloc", "calloc"]);
const OVERFLOW_MEM_FUNCS = new Set(["memcpy", "memmove", "memset"]);
const CMD_FUNCS = new Set([
    // Standard POSIX exec/spawn
    "system", "popen", "execl", "execlp", "execle", "execv", "execvp", "execve", "execvpe",
    // Uppercase macro variants (common in Juliet / NIST test suites)
    "SYSTEM", "POPEN", "EXECL", "EXECLP", "EXECLE", "EXECV", "EXECVP", "EXECVE",
    // Windows spawn family
    "_spawnl", "_spawnlp", "_spawnle", "_spawnlpe",
    "_spawnv", "_spawnvp", "_spawnve", "_spawnvpe",
    "posix_spawn", "posix_spawnp",
    // Uppercase spawn macros
    "SPAWNL", "SPAWNV", "SPAWNVP",
]);
const WEAK_HASH_FUNCS = new Set(["MD5", "EVP_md5"]);
const WEAK_HASH_SHA1 = new Set(["SHA1", "EVP_sha1"]);
const CRED_MACROS = /(PASSWORD|PASSWD|PWD|SECRET|API_KEY|APIKEY|TOKEN|AUTH_TOKEN|ACCESS_TOKEN|SECRET_KEY|CLIENT_SECRET|FALLBACK|KEY|PHRASE|PASSPHRASE|MATERIAL)/i;
// Windows Crypto API weak algorithm constants
const WEAK_CALG_CIPHER = new Set(["CALG_3DES", "CALG_3DES_112", "CALG_DES", "CALG_RC2", "CALG_RC4", "CALG_RC5"]);
const WEAK_CALG_HASH = new Set(["CALG_MD5", "CALG_MD4", "CALG_MD2", "CALG_SHA", "CALG_SHA1"]);
function analyzeC(code, filePath, tree) {
    const findings = [];
    const root = tree.rootNode;
    const freedPointers = new Map();
    // CWE-190 / CWE-787: taint-based integer / OOB detection
    const intTaint = new taint_1.TaintTracker();
    seedCIntegerSources(root, intTaint);
    seedCIntParamSources(root, intTaint); // treat int params as potential user input
    intTaint.propagateAssignments(root, isCIntegerSourceExpr);
    // CWE-78: string taint — track char* variables from user-controlled string sources
    const strTaint = new taint_1.TaintTracker();
    seedCStringSources(root, strTaint);
    strTaint.propagateAssignments(root, isCStringSourceExpr);
    for (const node of (0, taint_1.walkAll)(root)) {
        // CWE-190: arithmetic on user-controlled integer
        if (node.type === "init_declarator" || node.type === "assignment_expression") {
            const valueNode = node.type === "init_declarator"
                ? node.childForFieldName("value")
                : node.childForFieldName("right");
            if (valueNode && containsArithmetic(valueNode) && intTaint.expressionIsTainted(valueNode)
                && !isProtectedByBoundsCheck(node, valueNode)) {
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: "CWE-190", ruleId: "ast-integer-overflow",
                    vulnerability: "Integer Overflow",
                    severity: "medium",
                    message: "Arithmetic on user-controlled integer may overflow.",
                    filePath, node: valueNode, code,
                }));
            }
        }
        // CWE-190: x++ / x-- on tainted integer (update_expression)
        if (node.type === "update_expression") {
            const arg = node.children.find(c => c.type === "identifier");
            if (arg && intTaint.has(arg.text) && !isProtectedByBoundsCheck(node, arg)) {
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: "CWE-190", ruleId: "ast-integer-overflow",
                    vulnerability: "Integer Overflow",
                    severity: "medium",
                    message: `Increment/decrement of user-controlled integer '${arg.text}' may overflow.`,
                    filePath, node, code,
                }));
            }
        }
        // CWE-190: x += n / x -= n / x *= n (augmented_assignment on tainted var)
        if (node.type === "augmented_assignment_expression") {
            const left = node.childForFieldName("left");
            if (left?.type === "identifier" && intTaint.has(left.text) && !isProtectedByBoundsCheck(node, left)) {
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: "CWE-190", ruleId: "ast-integer-overflow",
                    vulnerability: "Integer Overflow",
                    severity: "medium",
                    message: `Augmented arithmetic on user-controlled integer '${left.text}' may overflow.`,
                    filePath, node, code,
                }));
            }
        }
    }
    for (const node of (0, taint_1.walkAll)(root)) {
        if (node.type === "call_expression") {
            const fnNode = node.childForFieldName("function");
            const argsNode = node.childForFieldName("arguments");
            const fnName = fnNode?.text ?? "";
            // CWE-787: out-of-bounds write
            if (OOB_WRITE_FUNCS.has(fnName)) {
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: "CWE-787", ruleId: "ast-oob-write",
                    vulnerability: "Out-of-bounds Write",
                    severity: "high",
                    message: `${fnName}() does not perform bounds checking and may write past a buffer.`,
                    filePath, node, code,
                }));
            }
            // Also catch scanf with %s
            if ((fnName === "scanf" || fnName === "fscanf" || fnName === "sscanf") && argsNode) {
                const args = getArgs(argsNode);
                const fmt = args.find(a => a.text.includes("%s"));
                if (fmt) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-787", ruleId: "ast-oob-write",
                        vulnerability: "Out-of-bounds Write",
                        severity: "high",
                        message: `${fnName}() with %s format specifier may write past buffer bounds.`,
                        filePath, node, code,
                    }));
                }
            }
            // CWE-787: strncpy(dest, src, strlen(src)) — copies source length into dest, ignores dest size
            if (fnName === "strncpy" && argsNode) {
                const args = getArgs(argsNode);
                if (args.length >= 3 && args[2].type === "call_expression") {
                    const sizeCallFn = args[2].childForFieldName("function")?.text ?? "";
                    if (sizeCallFn === "strlen") {
                        findings.push((0, utils_1.makeAstFinding)({
                            cweId: "CWE-787", ruleId: "ast-oob-write",
                            vulnerability: "Out-of-bounds Write",
                            severity: "high",
                            message: "strncpy() with strlen() as size copies based on source length, not destination size.",
                            filePath, node, code,
                        }));
                    }
                }
            }
            // CWE-78: command injection
            if (CMD_FUNCS.has(fnName) && argsNode) {
                const args = getArgs(argsNode);
                if (args.length > 0) {
                    // For system/popen: the entire first arg is the shell command — flag if non-literal
                    const isShellFunc = fnName.toLowerCase() === "system" || fnName.toLowerCase() === "popen";
                    if (isShellFunc) {
                        if (!isStringLiteral(args[0]) && !isNullOrConstant(args[0]) && !strTaint.has(args[0].text)) {
                            findings.push((0, utils_1.makeAstFinding)({
                                cweId: "CWE-78", ruleId: "ast-cmd-injection",
                                vulnerability: "OS Command Injection",
                                severity: "high",
                                message: `${fnName}() receives a non-literal command argument.`,
                                filePath, node, code,
                            }));
                        }
                    }
                    else {
                        // For exec/spawn family: flag only if the program path (first arg after any mode flag)
                        // is tainted, OR if a tainted string variable appears in any arg
                        const pathArgIdx = fnName.startsWith("_spawn") ? 1 : 0; // _spawnX has mode as arg[0]
                        const pathArg = args[pathArgIdx];
                        const anyTainted = args.some(a => strTaint.expressionIsTainted(a) || intTaint.expressionIsTainted(a));
                        if (anyTainted || (pathArg && !isStringLiteral(pathArg) && !isNullOrConstant(pathArg))) {
                            findings.push((0, utils_1.makeAstFinding)({
                                cweId: "CWE-78", ruleId: "ast-cmd-injection",
                                vulnerability: "OS Command Injection",
                                severity: "high",
                                message: `${fnName}() receives user-controlled argument.`,
                                filePath, node, code,
                            }));
                        }
                    }
                }
            }
            // CWE-190: integer overflow in allocation/memory functions
            if (OVERFLOW_ALLOC_FUNCS.has(fnName) && argsNode) {
                const args = getArgs(argsNode);
                const sizeArg = fnName === "realloc" ? args[1] : args[0];
                if (sizeArg && containsArithmetic(sizeArg) && !isProtectedByBoundsCheck(node, sizeArg)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-190", ruleId: "ast-integer-overflow",
                        vulnerability: "Integer Overflow",
                        severity: "medium",
                        message: `${fnName}() size argument contains arithmetic that may overflow.`,
                        filePath, node: sizeArg, code,
                    }));
                }
            }
            if (OVERFLOW_MEM_FUNCS.has(fnName) && argsNode) {
                const args = getArgs(argsNode);
                const sizeArg = args[2];
                if (sizeArg && containsArithmetic(sizeArg) && !isProtectedByBoundsCheck(node, sizeArg)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-190", ruleId: "ast-integer-overflow",
                        vulnerability: "Integer Overflow",
                        severity: "medium",
                        message: `${fnName}() size argument contains arithmetic that may overflow.`,
                        filePath, node: sizeArg, code,
                    }));
                }
            }
            // CWE-416: use-after-free — track free() calls
            if (fnName === "free" && argsNode) {
                const args = getArgs(argsNode);
                if (args.length > 0 && args[0].type === "identifier") {
                    freedPointers.set(args[0].text, node);
                }
            }
            // CWE-327: weak crypto
            if (WEAK_HASH_FUNCS.has(fnName)) {
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: "CWE-327", ruleId: "ast-weak-hash",
                    vulnerability: "Use of Broken Cryptographic Algorithm",
                    severity: "medium",
                    message: `${fnName}() uses MD5, a weak hashing algorithm.`,
                    filePath, node, code,
                }));
            }
            if (WEAK_HASH_SHA1.has(fnName)) {
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: "CWE-327", ruleId: "ast-weak-hash-sha1",
                    vulnerability: "Use of Broken Cryptographic Algorithm",
                    severity: "medium",
                    message: `${fnName}() uses SHA-1, a weak hashing algorithm.`,
                    filePath, node, code,
                }));
            }
            // CWE-327: Windows Crypto API — CryptDeriveKey/CryptEncrypt with weak cipher
            if ((fnName === "CryptDeriveKey" || fnName === "CryptEncrypt" || fnName === "CryptDecrypt") && argsNode) {
                const args = getArgs(argsNode);
                const algoArg = args[1]; // second arg is the algorithm constant
                if (algoArg && WEAK_CALG_CIPHER.has(algoArg.text)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-327", ruleId: "ast-weak-wincrypt-cipher",
                        vulnerability: "Use of Broken Cryptographic Algorithm",
                        severity: "medium",
                        message: `${fnName}() uses ${algoArg.text}, a weak or broken cipher.`,
                        filePath, node: algoArg, code,
                    }));
                }
            }
            // CWE-327: Windows Crypto API — CryptCreateHash with weak hash
            if (fnName === "CryptCreateHash" && argsNode) {
                const args = getArgs(argsNode);
                const algoArg = args[1]; // second arg is the algorithm constant
                if (algoArg && WEAK_CALG_HASH.has(algoArg.text)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-327", ruleId: "ast-weak-wincrypt-hash",
                        vulnerability: "Use of Broken Cryptographic Algorithm",
                        severity: "medium",
                        message: `CryptCreateHash() uses ${algoArg.text}, a weak hashing algorithm.`,
                        filePath, node: algoArg, code,
                    }));
                }
            }
        }
        // CWE-787: array subscript write with tainted index — arr[user_input] = val
        if (node.type === "assignment_expression") {
            const left = node.childForFieldName("left");
            if (left?.type === "subscript_expression") {
                const index = left.childForFieldName("index");
                if (index && intTaint.expressionIsTainted(index) && !isProtectedByBoundsCheck(node, index)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-787", ruleId: "ast-oob-write",
                        vulnerability: "Out-of-bounds Write",
                        severity: "high",
                        message: "Array write uses user-controlled index without bounds check.",
                        filePath, node: index, code,
                    }));
                }
            }
            // CWE-787: pointer arithmetic write — *(ptr + user_input) = val
            if (left?.type === "pointer_expression" || left?.type === "unary_expression") {
                const arg = left.children.find(c => c.type !== "*" && c.type !== "(" && c.type !== ")");
                if (arg && intTaint.expressionIsTainted(arg) && !isProtectedByBoundsCheck(node, arg)) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-787", ruleId: "ast-oob-write",
                        vulnerability: "Out-of-bounds Write",
                        severity: "high",
                        message: "Pointer write uses user-controlled offset without bounds check.",
                        filePath, node: arg, code,
                    }));
                }
            }
        }
        // CWE-787: loop with user-controlled bound writing to array
        if (node.type === "for_statement" || node.type === "while_statement") {
            const condition = node.childForFieldName("condition");
            if (condition && intTaint.expressionIsTainted(condition)) {
                const body = node.childForFieldName("body");
                if (body) {
                    for (const inner of (0, taint_1.walkAll)(body)) {
                        if (inner.type === "assignment_expression") {
                            const left = inner.childForFieldName("left");
                            if (left?.type === "subscript_expression" || left?.type === "pointer_expression") {
                                findings.push((0, utils_1.makeAstFinding)({
                                    cweId: "CWE-787", ruleId: "ast-oob-write",
                                    vulnerability: "Out-of-bounds Write",
                                    severity: "high",
                                    message: "Loop with user-controlled bound writes to array without bounds check.",
                                    filePath, node: condition, code,
                                }));
                                break;
                            }
                        }
                    }
                }
            }
        }
        // CWE-416: use-after-free — detect use of freed pointer
        if (node.type === "identifier" && freedPointers.has(node.text)) {
            const parent = node.parent;
            if (parent && !isFreeCall(parent) && !isAssignmentTarget(parent, node)) {
                const freeNode = freedPointers.get(node.text);
                if (node.startIndex > freeNode.startIndex) {
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: "CWE-416", ruleId: "ast-use-after-free",
                        vulnerability: "Use After Free",
                        severity: "high",
                        message: `Pointer '${node.text}' is used after being freed.`,
                        filePath, node, code,
                    }));
                    freedPointers.delete(node.text);
                }
            }
        }
        // Reset freed pointer if reassigned
        if (node.type === "assignment_expression") {
            const left = node.childForFieldName("left");
            if (left && freedPointers.has(left.text)) {
                freedPointers.delete(left.text);
            }
        }
        // CWE-259: hardcoded credentials in #define macros
        if (node.type === "preproc_def") {
            const nameNode = node.childForFieldName("name");
            const valueNode = node.childForFieldName("value");
            if (nameNode && valueNode && CRED_MACROS.test(nameNode.text)) {
                const val = valueNode.text.trim();
                if ((val.startsWith('"') || val.startsWith('L"') || val.startsWith('u"') || val.startsWith('U"')) && val.length > 5) {
                    const cwe = /KEY|SECRET|TOKEN/i.test(nameNode.text) ? "CWE-321" : "CWE-259";
                    findings.push((0, utils_1.makeAstFinding)({
                        cweId: cwe, ruleId: "ast-hardcoded-cred",
                        vulnerability: cwe === "CWE-321" ? "Use of Hard-coded Cryptographic Key" : "Use of Hard-coded Password",
                        severity: "high",
                        message: `Hard-coded credential in macro '${nameNode.text}'.`,
                        filePath, node: valueNode, code,
                    }));
                }
            }
        }
    }
    // CWE-190: constant overflow (CHAR_MAX/INT_MAX arithmetic, no user input needed)
    findings.push(...findConstantOverflows(root, filePath, code));
    return findings;
}
function getArgs(argsNode) {
    return argsNode.children.filter(c => c.type !== "," && c.type !== "(" && c.type !== ")");
}
function isStringLiteral(node) {
    return node.type === "string_literal" || node.type === "concatenated_string";
}
// NULL pointer, numeric literals, or ALL_CAPS constants (macro-defined path/flag constants)
function isNullOrConstant(node) {
    if (node.type === "null" || node.text === "NULL")
        return true;
    if (node.type === "number_literal")
        return true;
    // ALL_CAPS identifiers are typically #define constants (e.g. CMD_PATH, _P_WAIT)
    if (node.type === "identifier" && /^[A-Z_][A-Z0-9_]*$/.test(node.text))
        return true;
    return false;
}
function containsArithmetic(node) {
    if (node.type === "binary_expression") {
        const op = node.children.find(c => c.type === "+" || c.type === "*" || c.type === "-");
        if (op)
            return true;
    }
    if (node.type === "update_expression")
        return true;
    return node.children.some(c => containsArithmetic(c));
}
function isProtectedByBoundsCheck(callNode, sizeArg) {
    const vars = collectIdentifiers(sizeArg);
    if (vars.size === 0)
        return false;
    let cursor = callNode.parent;
    let depth = 0;
    while (cursor && depth < 15) {
        if (cursor.type === "if_statement") {
            const condition = cursor.childForFieldName("condition");
            if (condition) {
                const ctext = condition.text;
                // Only consider it protected if the check involves INT_MAX/UINT_MAX or explicit division
                // (prevents range checks like "x > 0" from masking real overflows)
                if (/INT_MAX|UINT_MAX|INT_MIN|SIZE_MAX/.test(ctext)) {
                    for (const v of vars) {
                        if (new RegExp(`\\b${v}\\b`).test(ctext))
                            return true;
                    }
                }
            }
        }
        cursor = cursor.parent;
        depth++;
    }
    return false;
}
function collectIdentifiers(node) {
    const ids = new Set();
    for (const n of (0, taint_1.walkAll)(node)) {
        if (n.type === "identifier")
            ids.add(n.text);
    }
    return ids;
}
function seedCIntegerSources(root, taint) {
    for (const node of (0, taint_1.walkAll)(root)) {
        if (node.type !== "call_expression")
            continue;
        const fn = node.childForFieldName("function")?.text ?? "";
        const argsNode = node.childForFieldName("arguments");
        if (!argsNode)
            continue;
        if (fn === "scanf" || fn === "fscanf" || fn === "sscanf") {
            for (const m of argsNode.text.matchAll(/&([a-zA-Z_][a-zA-Z0-9_]*)/g)) {
                taint.add(m[1]);
            }
        }
    }
}
// Seed integer-typed formal parameters as potentially user-controlled
const C_INT_TYPES = /^(int|size_t|ssize_t|long|unsigned|uint32_t|uint64_t|int32_t|int64_t|ptrdiff_t)$/;
function seedCIntParamSources(root, taint) {
    for (const node of (0, taint_1.walkAll)(root)) {
        if (node.type !== "function_definition")
            continue;
        const declarator = node.childForFieldName("declarator");
        if (!declarator)
            continue;
        // Find the parameter_list inside the declarator
        for (const child of (0, taint_1.walkAll)(declarator)) {
            if (child.type !== "parameter_declaration")
                continue;
            const type = child.childForFieldName("type")?.text ?? "";
            if (!C_INT_TYPES.test(type.trim()))
                continue;
            // The parameter name is the last identifier child
            const decl = child.childForFieldName("declarator");
            const name = decl?.type === "identifier" ? decl.text : decl?.children.find(c => c.type === "identifier")?.text;
            if (name)
                taint.add(name);
        }
    }
}
function isCIntegerSourceExpr(node) {
    const text = node.text;
    return /\batoi\s*\(/.test(text) ||
        /\bstrtol\s*\(/.test(text) ||
        /\bstrtoul\s*\(/.test(text) ||
        /\batol\s*\(/.test(text) ||
        /\bstrtoll\s*\(/.test(text) ||
        /\bstrtoull\s*\(/.test(text) ||
        /\bgetenv\s*\(/.test(text) ||
        /\brand\s*\(/.test(text) ||
        /\brand_r\s*\(/.test(text) ||
        /\brecv\s*\(/.test(text) ||
        /\bread\s*\(/.test(text) ||
        /\bfread\s*\(/.test(text) ||
        /\bfgets\s*\(/.test(text) ||
        /\bgetchar\s*\(/.test(text) ||
        /\bgetc\s*\(/.test(text);
}
// CWE-190: constant overflow detection — track variables assigned MAX/boundary constants
const OVERFLOW_CONST_PATTERN = /\b(CHAR_MAX|SCHAR_MAX|UCHAR_MAX|SHRT_MAX|USHRT_MAX|INT_MAX|UINT_MAX|LONG_MAX|ULONG_MAX|LLONG_MAX|ULLONG_MAX|INT8_MAX|INT16_MAX|INT32_MAX|INT64_MAX|UINT8_MAX|UINT16_MAX|UINT32_MAX|UINT64_MAX|SIZE_MAX)\b/;
function findConstantOverflows(root, filePath, code) {
    const findings = [];
    // Map variable name → node where it was assigned a MAX constant
    const maxVars = new Map();
    for (const node of (0, taint_1.walkAll)(root)) {
        // Seed: variable assigned to MAX constant directly (int x = INT_MAX or x = CHAR_MAX)
        if (node.type === "init_declarator" || node.type === "assignment_expression") {
            const lhs = node.type === "init_declarator"
                ? (() => { const d = node.childForFieldName("declarator"); return d?.type === "identifier" ? d : null; })()
                : node.childForFieldName("left");
            const rhs = node.type === "init_declarator"
                ? node.childForFieldName("value")
                : node.childForFieldName("right");
            if (lhs?.type === "identifier" && rhs && OVERFLOW_CONST_PATTERN.test(rhs.text)) {
                maxVars.set(lhs.text, rhs);
            }
        }
    }
    if (maxVars.size === 0)
        return findings;
    for (const node of (0, taint_1.walkAll)(root)) {
        if (node.type !== "init_declarator" && node.type !== "assignment_expression")
            continue;
        const valueNode = node.type === "init_declarator"
            ? node.childForFieldName("value")
            : node.childForFieldName("right");
        if (!valueNode)
            continue;
        if (!containsArithmetic(valueNode))
            continue;
        // Check if any MAX variable is referenced in this arithmetic expression
        const ids = collectIdentifiers(valueNode);
        for (const id of ids) {
            if (maxVars.has(id)) {
                findings.push((0, utils_1.makeAstFinding)({
                    cweId: "CWE-190", ruleId: "ast-integer-overflow",
                    vulnerability: "Integer Overflow",
                    severity: "medium",
                    message: `Arithmetic on '${id}' (assigned a boundary constant) may overflow.`,
                    filePath, node: valueNode, code,
                }));
                break;
            }
        }
    }
    return findings;
}
function seedCStringSources(root, taint) {
    for (const node of (0, taint_1.walkAll)(root)) {
        if (node.type !== "call_expression")
            continue;
        const fn = node.childForFieldName("function")?.text ?? "";
        const argsNode = node.childForFieldName("arguments");
        if (!argsNode)
            continue;
        // fgets(buf, size, stream) / gets(buf) — first arg is the destination buffer
        if (fn === "fgets" || fn === "gets") {
            const args = getArgs(argsNode);
            if (args.length > 0 && args[0].type === "identifier") {
                taint.add(args[0].text);
            }
        }
        // scanf/fscanf/sscanf — address-of args are destination buffers
        if (fn === "scanf" || fn === "fscanf" || fn === "sscanf") {
            for (const m of argsNode.text.matchAll(/&([a-zA-Z_][a-zA-Z0-9_]*)/g)) {
                taint.add(m[1]);
            }
        }
        // recv(sock, buf, ...) — second arg is the buffer
        if (fn === "recv" || fn === "read") {
            const args = getArgs(argsNode);
            if (args.length >= 2 && args[1].type === "identifier") {
                taint.add(args[1].text);
            }
        }
        // getenv returns a char* from environment — assign target is tainted
    }
    // getenv: the return value is tainted — caught via propagateAssignments with isCStringSourceExpr
}
function isCStringSourceExpr(node) {
    const text = node.text;
    return /\bgetenv\s*\(/.test(text) ||
        /\bgetlogin\s*\(/.test(text) ||
        /\bcuserid\s*\(/.test(text) ||
        /\bgetcwd\s*\(/.test(text);
}
function isFreeCall(node) {
    return node.type === "call_expression" &&
        node.childForFieldName("function")?.text === "free";
}
function isAssignmentTarget(parent, node) {
    if (parent.type === "assignment_expression") {
        const left = parent.childForFieldName("left");
        return left === node;
    }
    return false;
}
//# sourceMappingURL=c.js.map