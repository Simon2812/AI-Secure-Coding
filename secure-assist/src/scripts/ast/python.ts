import type { Node, Tree } from "web-tree-sitter";
import { Finding } from "../../analyzer/types";
import { TaintTracker, walkAll } from "./taint";
import { makeAstFinding } from "./utils";

const USER_INPUT_CALLS = new Set([
  "input", "sys.argv",
]);

const USER_INPUT_ATTRS = new Set([
  "args", "form", "files", "values", "json", "data",
]);

const PATH_SINKS = new Set([
  "open", "os.open", "codecs.open", "io.open",
  "send_file", "send_from_directory",
  "os.path.join", "os.path.abspath", "os.path.realpath",
  "shutil.copy", "shutil.copyfile", "shutil.move",
  "zipfile.ZipFile", "tarfile.open",
  "pathlib.Path", "Path",
]);

// Sinks where ANY arg (not just first) can be tainted
const PATH_SINKS_ANY_ARG = new Set(["os.path.join", "os.path.abspath", "os.path.realpath"]);

const CMD_SINKS = new Set([
  "os.system", "os.popen",
  "subprocess.run", "subprocess.Popen", "subprocess.call",
  "subprocess.check_call", "subprocess.check_output",
]);

const WEAK_HASH = new Set(["hashlib.md5", "hashlib.sha1", "hashlib.new"]);
const WEAK_CIPHER = new Set(["DES.new", "Crypto.Cipher.DES"]);

export function analyzePython(code: string, filePath: string, tree: Tree): Finding[] {
  const findings: Finding[] = [];
  const root = tree.rootNode;
  const taint = new TaintTracker();

  seedPythonTaint(root, taint);
  taint.propagateAssignments(root, isPythonUserInputExpr);
  propagatePythonCollections(root, taint);
  taint.propagateAssignments(root, isPythonUserInputExpr);

  const valueMap = buildPythonValueMap(root);

  for (const node of walkAll(root)) {

    // CWE-22: pathlib / operator — base / tainted_var
    if (node.type === "binary_operator") {
      const op = node.children.find(c => c.type === "/");
      if (op) {
        const right = node.childForFieldName("right");
        if (right && (taint.expressionIsTainted(right) || isPythonUserInputExpr(right))) {
          findings.push(makeAstFinding({
            cweId: "CWE-22", ruleId: "ast-path-traversal",
            vulnerability: "Path Traversal",
            severity: "high",
            message: "pathlib path join with user-controlled input may allow path traversal.",
            filePath, node: right, code,
          }));
        }
      }
    }

    if (node.type !== "call") continue;

    const fnName = callName(node);
    const args = callArgs(node);

    // CWE-22: path traversal
    if (fnName && PATH_SINKS.has(fnName) && args.length > 0) {
      const checkArgs = PATH_SINKS_ANY_ARG.has(fnName) ? args : [args[0]];
      const taintedArg = checkArgs.find(a => taint.expressionIsTainted(a) || isPythonUserInputExpr(a));
      if (taintedArg) {
        findings.push(makeAstFinding({
          cweId: "CWE-22", ruleId: "ast-path-traversal",
          vulnerability: "Path Traversal",
          severity: "high",
          message: `${fnName}() receives user-controlled path without validation.`,
          filePath, node: taintedArg, code,
        }));
      }
    }

    // CWE-78: command injection
    if (fnName && CMD_SINKS.has(fnName) && args.length > 0) {
      const firstArg = args[0];
      if (firstArg.type !== "list" && (taint.expressionIsTainted(firstArg) || isPythonUserInputExpr(firstArg))) {
        findings.push(makeAstFinding({
          cweId: "CWE-78", ruleId: "ast-cmd-injection",
          vulnerability: "OS Command Injection",
          severity: "high",
          message: `${fnName}() receives user-controlled input.`,
          filePath, node: firstArg, code,
        }));
      }
    }

    // CWE-89: SQL injection — unwrap text()/literal() wrappers (SQLAlchemy)
    if (fnName?.endsWith(".execute") && args.length > 0) {
      let queryArg = args[0];
      // Unwrap text(f"...") / literal(f"...") → check inner arg
      if ((queryArg.type === "call") && /^(text|literal|sql)$/.test(callName(queryArg) ?? "")) {
        const innerArgs = callArgs(queryArg);
        if (innerArgs.length > 0) queryArg = innerArgs[0];
      }
      if (hasUnsafeSqlConstruction(queryArg, taint, valueMap)) {
        findings.push(makeAstFinding({
          cweId: "CWE-89", ruleId: "ast-sqli",
          vulnerability: "SQL Injection",
          severity: "high",
          message: "SQL query is constructed with user-controlled input.",
          filePath, node: queryArg, code,
        }));
      }
    }

    // CWE-327/328: weak crypto
    if (fnName && WEAK_HASH.has(fnName)) {
      findings.push(makeAstFinding({
        cweId: "CWE-327", ruleId: "ast-weak-hash",
        vulnerability: "Use of Broken Cryptographic Algorithm",
        severity: "medium",
        message: `${fnName}() uses a weak hashing algorithm.`,
        filePath, node, code,
      }));
    }
    if (fnName && WEAK_CIPHER.has(fnName)) {
      findings.push(makeAstFinding({
        cweId: "CWE-327", ruleId: "ast-weak-cipher",
        vulnerability: "Use of Broken Cryptographic Algorithm",
        severity: "medium",
        message: `${fnName}() uses DES, an insecure cipher.`,
        filePath, node, code,
      }));
    }
  }

  // CWE-259/321: hardcoded credentials
  findings.push(...findHardcodedCredentialsPython(root, filePath, code));

  return findings;
}

function seedPythonTaint(root: Node, taint: TaintTracker): void {
  for (const node of walkAll(root)) {
    // Direct assignment from user input expression
    if (node.type === "assignment") {
      const lhs = node.childForFieldName("left");
      const rhs = node.childForFieldName("right");
      if (lhs?.type === "identifier" && rhs && isPythonUserInputExpr(rhs)) {
        taint.add(lhs.text);
      }
    }
    // for key in request.form.keys(): → key is tainted
    if (node.type === "for_statement") {
      const left = node.childForFieldName("left");
      const right = node.childForFieldName("right");
      if (left?.type === "identifier" && right && isPythonUserInputExpr(right)) {
        taint.add(left.text);
      }
    }
  }
}

// Propagate taint through collection mutations and dict subscript writes
function propagatePythonCollections(root: Node, taint: TaintTracker): void {
  let changed = true;
  while (changed) {
    changed = false;
    for (const node of walkAll(root)) {
      // dict["key"] = tainted_expr → dict tainted
      if (node.type === "assignment") {
        const lhs = node.childForFieldName("left");
        const rhs = node.childForFieldName("right");
        if (lhs?.type === "subscript" && rhs && taint.expressionIsTainted(rhs)) {
          const dictObj = lhs.childForFieldName("value");
          if (dictObj?.type === "identifier" && !taint.has(dictObj.text)) {
            taint.add(dictObj.text);
            changed = true;
          }
        }
      }
      // list.append(tainted) / list.insert(n, tainted) / list.extend(tainted) → list tainted
      if (node.type === "call") {
        const fn = node.childForFieldName("function");
        if (fn?.type === "attribute") {
          const method = fn.childForFieldName("attribute")?.text ?? "";
          const obj = fn.childForFieldName("object");
          if (obj?.type === "identifier" && !taint.has(obj.text)) {
            const args = callArgs(node);
            if ((method === "append" || method === "add" || method === "extend") && args.length > 0
                && taint.expressionIsTainted(args[args.length - 1])) {
              taint.add(obj.text);
              changed = true;
            }
            if (method === "insert" && args.length > 1 && taint.expressionIsTainted(args[1])) {
              taint.add(obj.text);
              changed = true;
            }
            if ((method === "update" || method === "setdefault") && args.some(a => taint.expressionIsTainted(a))) {
              taint.add(obj.text);
              changed = true;
            }
          }
        }
      }
      // for item in tainted_list: → item tainted
      if (node.type === "for_statement") {
        const left = node.childForFieldName("left");
        const right = node.childForFieldName("right");
        if (left?.type === "identifier" && right && taint.expressionIsTainted(right) && !taint.has(left.text)) {
          taint.add(left.text);
          changed = true;
        }
      }
    }
  }
}

function isPythonUserInputExpr(node: Node): boolean {
  const text = node.text;
  if (/\binput\s*\(/.test(text)) return true;
  if (/\bsys\.argv\b/.test(text)) return true;
  if (/\brequest\.(args|form|files|values|json|data|get_json|cookies)\b/.test(text)) return true;
  if (/\brequest\[/.test(text)) return true;
  if (/\burllib\.parse\.unquote/.test(text)) return true;
  if (/\burllib\.parse\.unquote_plus/.test(text)) return true;
  if (/\bos\.environ\b/.test(text)) return true;
  if (/\bos\.getenv\s*\(/.test(text)) return true;
  return false;
}

function callName(node: Node): string | null {
  const fn = node.childForFieldName("function");
  if (!fn) return null;
  return fn.text;
}

function callArgs(node: Node): Node[] {
  const argList = node.childForFieldName("arguments");
  if (!argList) return [];
  return argList.children.filter(c => c.type !== "," && c.type !== "(" && c.type !== ")");
}

function hasUnsafeSqlConstruction(node: Node, taint: TaintTracker, valueMap?: Map<string, Node>): boolean {
  // Tainted or resolvable identifier
  if (node.type === "identifier") {
    if (taint.expressionIsTainted(node)) return true;
    const resolved = valueMap?.get(node.text);
    if (resolved && resolved !== node) return hasUnsafeSqlConstruction(resolved, taint, valueMap);
    return false;
  }

  const text = node.text.toLowerCase();
  if (!/\b(select|insert|update|delete)\b/.test(text)) return false;
  if (node.type === "string") return false;
  if (taint.expressionIsTainted(node)) return true;
  if (node.type === "binary_operator" || node.type === "concatenated_string") return true;
  if (node.type === "formatted_string" || node.type === "f_string") return true;
  if (/\.format\s*\(/.test(node.text) || /\s*%\s*/.test(node.text)) return true;
  return false;
}

function buildPythonValueMap(root: Node): Map<string, Node> {
  const map = new Map<string, Node>();
  for (const node of walkAll(root)) {
    if (node.type === "assignment") {
      const lhs = node.childForFieldName("left");
      const rhs = node.childForFieldName("right");
      if (lhs?.type === "identifier" && rhs) map.set(lhs.text, rhs);
    }
  }
  return map;
}

function findHardcodedCredentialsPython(
  root: Node, filePath: string, code: string
): Finding[] {
  const findings: Finding[] = [];
  const credVars = /^(password|passwd|pwd|secret|api_key|apikey|token|auth_token|access_token|secret_key|client_secret)$/i;

  for (const node of walkAll(root)) {
    if (node.type !== "assignment") continue;
    const lhs = node.childForFieldName("left");
    const rhs = node.childForFieldName("right");
    if (!lhs || !rhs) continue;
    if (!credVars.test(lhs.text)) continue;
    if (rhs.type === "string" && rhs.text.length > 5) {
      const cwe = /key|secret|token/.test(lhs.text.toLowerCase()) ? "CWE-321" : "CWE-259";
      findings.push(makeAstFinding({
        cweId: cwe, ruleId: "ast-hardcoded-cred",
        vulnerability: cwe === "CWE-321" ? "Use of Hard-coded Cryptographic Key" : "Use of Hard-coded Password",
        severity: "high",
        message: `Hard-coded credential assigned to '${lhs.text}'.`,
        filePath, node: rhs, code,
      }));
    }
  }
  return findings;
}
