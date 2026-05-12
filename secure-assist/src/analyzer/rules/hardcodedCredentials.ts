import { RuleContext, Finding } from "../types";
import { createFinding } from "../utils";

export function findHardcodedCredentials(context: RuleContext): Finding[] {
  const findings: Finding[] = [];
  const { code, filePath } = context;

  const patterns = [
    {
      ruleId: "hardcoded-password",
      cweId: "CWE-259",
      vulnerability: "Use of Hard-coded Password",
      severity: "high" as const,
      regex: /\b(password|passwd|pwd)\b\s*[:=]\s*["'`][^"'`\n]{3,}["'`]/gi,
      message: "Possible hard-coded password found in source code.",
    },
    {
      ruleId: "hardcoded-password-define",
      cweId: "CWE-259",
      vulnerability: "Use of Hard-coded Password",
      severity: "high" as const,
      regex: /^#define\s+(PASSWORD|PASSWD|PWD)[A-Z0-9_]*\s+L?"[^"\n]{3,}"/gim,
      message: "Possible hard-coded password in preprocessor macro.",
    },
    {
      ruleId: "hardcoded-password-dict",
      cweId: "CWE-259",
      vulnerability: "Use of Hard-coded Password",
      severity: "high" as const,
      regex: /"(password|passwd|pwd)"\s*[:]\s*"[^"\n]{3,}"/gi,
      message: "Possible hard-coded password in dictionary or map literal.",
    },
    {
      ruleId: "hardcoded-api-key",
      cweId: "CWE-321",
      vulnerability: "Use of Hard-coded Cryptographic Key",
      severity: "high" as const,
      regex: /\b(api[_-]?key|apikey|client[_-]?secret|secret[_-]?key)\b\s*[:=]\s*["'`][^"'`\n]{6,}["'`]/gi,
      message: "Possible hard-coded API key or secret found in source code.",
    },
    {
      ruleId: "hardcoded-api-key-define",
      cweId: "CWE-321",
      vulnerability: "Use of Hard-coded Cryptographic Key",
      severity: "high" as const,
      regex: /^#define\s+(API_?KEY|SECRET_?KEY|CLIENT_?SECRET|AUTH_?TOKEN|ACCESS_?TOKEN)[A-Z0-9_]*\s+L?"[^"\n]{6,}"/gim,
      message: "Possible hard-coded cryptographic key in preprocessor macro.",
    },
    {
      ruleId: "hardcoded-token",
      cweId: "CWE-321",
      vulnerability: "Use of Hard-coded Cryptographic Key",
      severity: "high" as const,
      regex: /\b(token|access[_-]?token|auth[_-]?token)\b\s*[:=]\s*["'`][^"'`\n]{6,}["'`]/gi,
      message: "Possible hard-coded authentication token found in source code.",
    },
  ];

  for (const pattern of patterns) {
    for (const match of code.matchAll(pattern.regex)) {
      if (match.index === undefined) continue;

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