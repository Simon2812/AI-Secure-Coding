import type { Node, Tree } from "web-tree-sitter";
import { Finding } from "../../analyzer/types";
import { TaintTracker, walkAll } from "./taint";
import { makeAstFinding } from "./utils";

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

export function analyzeJava(code: string, filePath: string, tree: Tree): Finding[] {
  const findings: Finding[] = [];
  const root = tree.rootNode;
  const taint = new TaintTracker();

  seedJavaTaint(root, taint);
  taint.propagateAssignments(root, isJavaUserInputExpr);

  for (const node of walkAll(root)) {

    // object_creation_expression: new File(...), new ProcessBuilder(...)
    if (node.type === "object_creation_expression") {
      const typeNode = node.childForFieldName("type");
      const argsNode = node.childForFieldName("arguments");
      const typeName = typeNode?.text ?? "";

      if (PATH_SINK_TYPES.has(typeName) && argsNode) {
        const args = getJavaArgs(argsNode);
        if (args.length > 0 && (taint.expressionIsTainted(args[0]) || isJavaUserInputExpr(args[0]))) {
          findings.push(makeAstFinding({
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
          findings.push(makeAstFinding({
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
          findings.push(makeAstFinding({
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
          findings.push(makeAstFinding({
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
          findings.push(makeAstFinding({
            cweId: "CWE-327", ruleId: "ast-weak-hash",
            vulnerability: "Use of Broken Cryptographic Algorithm",
            severity: "medium",
            message: `getInstance(${args[0].text}) uses a weak algorithm.`,
            filePath, node, code,
          }));
        }
        if (args.length > 0 && WEAK_CIPHER_ALGOS.test(args[0].text)) {
          findings.push(makeAstFinding({
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
          findings.push(makeAstFinding({
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

function seedJavaTaint(root: Node, taint: TaintTracker): void {
  for (const node of walkAll(root)) {
    // local_variable_declaration: Type name = expr;
    if (node.type === "local_variable_declaration") {
      const declarator = node.children.find(c => c.type === "variable_declarator");
      if (!declarator) continue;
      const nameNode = declarator.childForFieldName("name");
      const valueNode = declarator.childForFieldName("value");
      if (!nameNode || !valueNode) continue;
      if (isJavaUserInputExpr(valueNode)) {
        taint.add(nameNode.text);
      }
      continue;
    }
    // assignment_expression: name = expr (inside loops, if-blocks, etc.)
    if (node.type === "assignment_expression") {
      const left = node.childForFieldName("left");
      const right = node.childForFieldName("right");
      if (!left || !right || left.type !== "identifier") continue;
      if (isJavaUserInputExpr(right)) {
        taint.add(left.text);
      }
    }
  }
}

function isJavaUserInputExpr(node: Node): boolean {
  const text = node.text;
  if (/\bgetParameter\s*\(/.test(text)) return true;
  if (/\bgetHeaders?\s*\(/.test(text)) return true;
  if (/\bgetQueryString\s*\(/.test(text)) return true;
  if (/\bgetPathInfo\s*\(/.test(text)) return true;
  if (/\bgetParts?\s*\(/.test(text)) return true;
  if (/\.getValue\s*\(/.test(text)) return true;
  if (/\.nextElement\s*\(/.test(text)) return true;
  if (/\.nextLine\s*\(/.test(text)) return true;
  if (/\.readLine\s*\(/.test(text)) return true;
  if (/\bargs\s*\[/.test(text)) return true;
  return false;
}

function getJavaArgs(argsNode: Node): Node[] {
  return argsNode.children.filter(c => c.type !== "," && c.type !== "(" && c.type !== ")");
}

function hasUnsafeSqlConstruction(node: Node, taint: TaintTracker): boolean {
  const text = node.text.toLowerCase();
  if (!/\b(select|insert|update|delete)\b/.test(text)) return false;
  if (node.type === "string_literal") return false;
  if (taint.expressionIsTainted(node)) return true;
  if (node.type === "binary_expression" && node.text.includes("+")) return true;
  if (/String\.format\s*\(/.test(node.text)) return true;
  return false;
}

function findHardcodedCredentialsJava(
  root: Node, filePath: string, code: string
): Finding[] {
  const findings: Finding[] = [];
  const credVars = /^(password|passwd|pwd|secret|apiKey|api_key|token|authToken|accessToken|secretKey|clientSecret)$/i;

  for (const node of walkAll(root)) {
    if (node.type !== "variable_declarator") continue;
    const nameNode = node.childForFieldName("name");
    const valueNode = node.childForFieldName("value");
    if (!nameNode || !valueNode) continue;
    if (!credVars.test(nameNode.text)) continue;
    if (valueNode.type === "string_literal" && valueNode.text.length > 5) {
      const cwe = /key|secret|token/i.test(nameNode.text) ? "CWE-321" : "CWE-259";
      findings.push(makeAstFinding({
        cweId: cwe, ruleId: "ast-hardcoded-cred",
        vulnerability: cwe === "CWE-321" ? "Use of Hard-coded Cryptographic Key" : "Use of Hard-coded Password",
        severity: "high",
        message: `Hard-coded credential assigned to '${nameNode.text}'.`,
        filePath, node: valueNode, code,
      }));
    }
  }
  return findings;
}
