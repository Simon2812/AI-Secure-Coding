import { RuleContext, Finding } from "../types";
import { createFinding } from "../utils";

export function findCommandInjection(context: RuleContext): Finding[] {
  const findings: Finding[] = [];
  const { code, filePath, language } = context;

  let patterns: Array<{
    ruleId: string;
    cweId: string;
    vulnerability: string;
    severity: "high";
    regex: RegExp;
    message: string;
  }> = [];

  if (language === "cpp") {
    patterns = [
      {
        ruleId: "cpp-system",
        cweId: "CWE-78",
        vulnerability: "OS Command Injection",
        severity: "high",
        regex: /\bsystem\s*\(/gi,
        message: "Use of system() may allow OS command injection if input is not controlled.",
      },
      {
        ruleId: "cpp-popen",
        cweId: "CWE-78",
        vulnerability: "OS Command Injection",
        severity: "high",
        regex: /\bpopen\s*\(/gi,
        message: "Use of popen() may allow OS command injection if input is not controlled.",
      },
      {
        ruleId: "cpp-exec",
        cweId: "CWE-78",
        vulnerability: "OS Command Injection",
        severity: "high",
        regex: /\b(execl|execlp|execle|execv|execvp|execve|execvpe)\s*\(/gi,
        message: "Use of exec*() may allow OS command injection if arguments are user-controlled.",
      },
      {
        ruleId: "cpp-spawn",
        cweId: "CWE-78",
        vulnerability: "OS Command Injection",
        severity: "high",
        regex: /\b(_spawnl|_spawnlp|_spawnle|_spawnlpe|_spawnv|_spawnvp|_spawnve|_spawnvpe|posix_spawn|posix_spawnp)\s*\(/gi,
        message: "Use of spawn*() may allow OS command injection if arguments are user-controlled.",
      },
    ];
  } else if (language === "java") {
    patterns = [
      {
        ruleId: "java-runtime-exec",
        cweId: "CWE-78",
        vulnerability: "OS Command Injection",
        severity: "high",
        regex: /\b[a-zA-Z_][a-zA-Z0-9_]*\s*\.\s*exec\s*\(/g,
        message: "Runtime.exec() may allow OS command injection if input is not controlled.",
      },
      {
        ruleId: "java-processbuilder",
        cweId: "CWE-78",
        vulnerability: "OS Command Injection",
        severity: "high",
        regex: /\bProcessBuilder\s*\(/g,
        message: "ProcessBuilder may allow OS command injection if arguments include unsafe input.",
      },
    ];
  } else if (language === "python") {
    patterns = [
      {
        ruleId: "python-os-system",
        cweId: "CWE-78",
        vulnerability: "OS Command Injection",
        severity: "high",
        regex: /\bos\.system\s*\(/g,
        message: "os.system() may allow OS command injection if input is not controlled.",
      },
      {
        ruleId: "python-subprocess",
        cweId: "CWE-78",
        vulnerability: "OS Command Injection",
        severity: "high",
        regex: /\bsubprocess\.(run|Popen|call|check_call|check_output)\s*\(/g,
        message: "subprocess execution may allow OS command injection if input is not controlled.",
      },
    ];
  }

  for (const pattern of patterns) {
    for (const match of code.matchAll(pattern.regex)) {
      if (match.index === undefined) continue;

      const afterCall = code.slice(match.index + match[0].length).trimStart();
      if (isSafeArgument(afterCall)) continue;

      findings.push(
        createFinding({
          cweId: pattern.cweId,
          ruleId: pattern.ruleId,
          vulnerability: pattern.vulnerability,
          severity: pattern.severity,
          message: pattern.message,
          file: filePath,
          code,
          index: match.index,
          evidence: match[0],
        })
      );
    }
  }

  return findings;
}

function isSafeArgument(textAfterOpenParen: string): boolean {
  const trimmed = textAfterOpenParen.trimStart();
  // List literal: subprocess.run(["cmd", "arg"])
  if (trimmed.startsWith("[")) return true;
  // Plain string literal with no format/concat: os.system("ls")
  if (/^["'][^"']*["']/.test(trimmed)) return true;
  return false;
}