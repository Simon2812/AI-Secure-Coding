import type { Node, Tree } from "web-tree-sitter";
import { Finding } from "../../analyzer/types";
import { TaintTracker, walkAll } from "./taint";
import { makeAstFinding } from "./utils";

const OOB_WRITE_FUNCS = new Set(["gets", "strcpy", "strcat", "sprintf", "vsprintf"]);
const OVERFLOW_ALLOC_FUNCS = new Set(["malloc", "realloc", "calloc"]);
const OVERFLOW_MEM_FUNCS = new Set(["memcpy", "memmove", "memset"]);
const CMD_FUNCS = new Set(["system", "popen", "execl", "execlp", "execv", "execvp"]);
const WEAK_HASH_FUNCS = new Set(["MD5", "EVP_md5"]);
const WEAK_HASH_SHA1 = new Set(["SHA1", "EVP_sha1"]);
const CRED_MACROS = /^(PASSWORD|PASSWD|PWD|SECRET|API_KEY|APIKEY|TOKEN|AUTH_TOKEN|ACCESS_TOKEN|SECRET_KEY|CLIENT_SECRET)/i;

export function analyzeC(code: string, filePath: string, tree: Tree): Finding[] {
  const findings: Finding[] = [];
  const root = tree.rootNode;
  const freedPointers = new Map<string, Node>();

  // CWE-190: taint-based integer overflow detection
  const intTaint = new TaintTracker();
  seedCIntegerSources(root, intTaint);
  intTaint.propagateAssignments(root, isCIntegerSourceExpr);

  for (const node of walkAll(root)) {
    // CWE-190: arithmetic on user-controlled integer
    if (node.type === "init_declarator" || node.type === "assignment_expression") {
      const valueNode = node.type === "init_declarator"
        ? node.childForFieldName("value")
        : node.childForFieldName("right");
      if (valueNode && containsArithmetic(valueNode) && intTaint.expressionIsTainted(valueNode)
          && !isProtectedByBoundsCheck(node, valueNode)) {
        findings.push(makeAstFinding({
          cweId: "CWE-190", ruleId: "ast-integer-overflow",
          vulnerability: "Integer Overflow",
          severity: "medium",
          message: "Arithmetic on user-controlled integer may overflow.",
          filePath, node: valueNode, code,
        }));
      }
    }
  }

  for (const node of walkAll(root)) {

    if (node.type === "call_expression") {
      const fnNode = node.childForFieldName("function");
      const argsNode = node.childForFieldName("arguments");
      const fnName = fnNode?.text ?? "";

      // CWE-787: out-of-bounds write
      if (OOB_WRITE_FUNCS.has(fnName)) {
        findings.push(makeAstFinding({
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
          findings.push(makeAstFinding({
            cweId: "CWE-787", ruleId: "ast-oob-write",
            vulnerability: "Out-of-bounds Write",
            severity: "high",
            message: `${fnName}() with %s format specifier may write past buffer bounds.`,
            filePath, node, code,
          }));
        }
      }

      // CWE-78: command injection
      if (CMD_FUNCS.has(fnName) && argsNode) {
        const args = getArgs(argsNode);
        if (args.length > 0 && !isStringLiteral(args[0])) {
          findings.push(makeAstFinding({
            cweId: "CWE-78", ruleId: "ast-cmd-injection",
            vulnerability: "OS Command Injection",
            severity: "high",
            message: `${fnName}() may allow command injection if argument is user-controlled.`,
            filePath, node, code,
          }));
        }
      }

      // CWE-190: integer overflow in allocation/memory functions
      if (OVERFLOW_ALLOC_FUNCS.has(fnName) && argsNode) {
        const args = getArgs(argsNode);
        const sizeArg = fnName === "realloc" ? args[1] : args[0];
        if (sizeArg && containsArithmetic(sizeArg) && !isProtectedByBoundsCheck(node, sizeArg)) {
          findings.push(makeAstFinding({
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
          findings.push(makeAstFinding({
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
        findings.push(makeAstFinding({
          cweId: "CWE-327", ruleId: "ast-weak-hash",
          vulnerability: "Use of Broken Cryptographic Algorithm",
          severity: "medium",
          message: `${fnName}() uses MD5, a weak hashing algorithm.`,
          filePath, node, code,
        }));
      }
      if (WEAK_HASH_SHA1.has(fnName)) {
        findings.push(makeAstFinding({
          cweId: "CWE-327", ruleId: "ast-weak-hash-sha1",
          vulnerability: "Use of Broken Cryptographic Algorithm",
          severity: "medium",
          message: `${fnName}() uses SHA-1, a weak hashing algorithm.`,
          filePath, node, code,
        }));
      }
    }

    // CWE-416: use-after-free — detect use of freed pointer
    if (node.type === "identifier" && freedPointers.has(node.text)) {
      const parent = node.parent;
      if (parent && !isFreeCall(parent) && !isAssignmentTarget(parent, node)) {
        const freeNode = freedPointers.get(node.text)!;
        if (node.startIndex > freeNode.startIndex) {
          findings.push(makeAstFinding({
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
        if ((val.startsWith('"') || val.startsWith('L"')) && val.length > 5) {
          const cwe = /KEY|SECRET|TOKEN/i.test(nameNode.text) ? "CWE-321" : "CWE-259";
          findings.push(makeAstFinding({
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

  return findings;
}

function getArgs(argsNode: Node): Node[] {
  return argsNode.children.filter(c => c.type !== "," && c.type !== "(" && c.type !== ")");
}

function isStringLiteral(node: Node): boolean {
  return node.type === "string_literal" || node.type === "concatenated_string";
}

function containsArithmetic(node: Node): boolean {
  if (node.type === "binary_expression") {
    const op = node.children.find(c => c.type === "+" || c.type === "*");
    if (op) return true;
  }
  return node.children.some(c => containsArithmetic(c));
}

function isProtectedByBoundsCheck(callNode: Node, sizeArg: Node): boolean {
  const vars = collectIdentifiers(sizeArg);
  if (vars.size === 0) return false;

  let cursor: Node | null = callNode.parent;
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
            if (new RegExp(`\\b${v}\\b`).test(ctext)) return true;
          }
        }
      }
    }
    cursor = cursor.parent;
    depth++;
  }
  return false;
}

function collectIdentifiers(node: Node): Set<string> {
  const ids = new Set<string>();
  for (const n of walkAll(node)) {
    if (n.type === "identifier") ids.add(n.text);
  }
  return ids;
}

function seedCIntegerSources(root: Node, taint: TaintTracker): void {
  for (const node of walkAll(root)) {
    if (node.type !== "call_expression") continue;
    const fn = node.childForFieldName("function")?.text ?? "";
    const argsNode = node.childForFieldName("arguments");
    if (!argsNode) continue;
    if (fn === "scanf" || fn === "fscanf" || fn === "sscanf") {
      for (const m of argsNode.text.matchAll(/&([a-zA-Z_][a-zA-Z0-9_]*)/g)) {
        taint.add(m[1]);
      }
    }
  }
}

function isCIntegerSourceExpr(node: Node): boolean {
  const text = node.text;
  return /\batoi\s*\(/.test(text) ||
         /\bstrtol\s*\(/.test(text) ||
         /\bstrtoul\s*\(/.test(text) ||
         /\batol\s*\(/.test(text) ||
         /\bgetenv\s*\(/.test(text);
}

function isFreeCall(node: Node): boolean {
  return node.type === "call_expression" &&
    node.childForFieldName("function")?.text === "free";
}

function isAssignmentTarget(parent: Node, node: Node): boolean {
  if (parent.type === "assignment_expression") {
    const left = parent.childForFieldName("left");
    return left === node;
  }
  return false;
}
