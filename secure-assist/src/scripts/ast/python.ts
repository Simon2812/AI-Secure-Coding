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
  "open", "os.open", "send_file", "send_from_directory",
  "shutil.copy", "shutil.copyfile", "shutil.move",
  "zipfile.ZipFile", "tarfile.open",
]);

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

  for (const node of walkAll(root)) {
    if (node.type !== "call") continue;

    const fnName = callName(node);
    const args = callArgs(node);

    // CWE-22: path traversal
    if (fnName && PATH_SINKS.has(fnName) && args.length > 0) {
      const firstArg = args[0];
      if (taint.expressionIsTainted(firstArg) || isPythonUserInputExpr(firstArg)) {
        findings.push(makeAstFinding({
          cweId: "CWE-22", ruleId: "ast-path-traversal",
          vulnerability: "Path Traversal",
          severity: "high",
          message: `${fnName}() receives user-controlled path without validation.`,
          filePath, node: firstArg, code,
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

    // CWE-89: SQL injection
    if (fnName?.endsWith(".execute") && args.length > 0) {
      const queryArg = args[0];
      if (hasUnsafeSqlConstruction(queryArg, taint)) {
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
    if (node.type !== "assignment") continue;
    const lhs = node.childForFieldName("left");
    const rhs = node.childForFieldName("right");
    if (!lhs || !rhs) continue;
    if (lhs.type === "identifier" && isPythonUserInputExpr(rhs)) {
      taint.add(lhs.text);
    }
  }
}

function isPythonUserInputExpr(node: Node): boolean {
  const text = node.text;
  if (/\binput\s*\(/.test(text)) return true;
  if (/\bsys\.argv\b/.test(text)) return true;
  if (/\brequest\.(args|form|files|values|json|data|get_json)\b/.test(text)) return true;
  if (/\brequest\[/.test(text)) return true;
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

function hasUnsafeSqlConstruction(node: Node, taint: TaintTracker): boolean {
  const text = node.text.toLowerCase();
  if (!/\b(select|insert|update|delete)\b/.test(text)) return false;
  if (node.type === "string") return false;
  if (taint.expressionIsTainted(node)) return true;
  if (node.type === "binary_operator" || node.type === "concatenated_string") return true;
  if (node.type === "formatted_string" || node.type === "f_string") return true;
  if (/\.format\s*\(/.test(node.text) || /\s*%\s*/.test(node.text)) return true;
  return false;
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
