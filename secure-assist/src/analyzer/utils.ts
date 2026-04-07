import { Finding, Severity } from "./types";

export function getLineAndColumn(text: string, index: number): { line: number; column: number } {
  const before = text.slice(0, index);
  const lines = before.split("\n");

  return {
    line: lines.length,
    column: lines[lines.length - 1].length + 1,
  };
}

export function createFinding(args: {
  cweId: string;
  ruleId: string;
  vulnerability: string;
  severity: Severity;
  message: string;
  file: string;
  code: string;
  index: number;
  evidence: string;
}): Finding {
  const pos = getLineAndColumn(args.code, args.index);

  return {
    cweId: args.cweId,
    ruleId: args.ruleId,
    vulnerability: args.vulnerability,
    severity: args.severity,
    message: args.message,
    file: args.file,
    line: pos.line,
    column: pos.column,
    evidence: args.evidence,
  };
}

export function detectLanguage(filePath: string): string {
  const lower = filePath.toLowerCase();

  if (lower.endsWith(".c") || lower.endsWith(".cpp") || lower.endsWith(".cc") || lower.endsWith(".cxx") || lower.endsWith(".h") || lower.endsWith(".hpp")) {
    return "cpp";
  }

  if (lower.endsWith(".java")) {
    return "java";
  }

  if (lower.endsWith(".py")) {
    return "python";
  }

  return "unknown";
}