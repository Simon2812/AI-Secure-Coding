import { RuleContext, Finding } from "../types";
import { createFinding } from "../utils";

export function findOutOfBoundsWrite(context: RuleContext): Finding[] {
  if (context.language !== "cpp") {
    return [];
  }

  const findings: Finding[] = [];
  const { code, filePath } = context;

  const dangerousPatterns = [
    /\bgets\s*\(([^)]*)\)/g,
    /\bstrcpy\s*\(([^)]*)\)/g,
    /\bstrcat\s*\(([^)]*)\)/g,
    /\bsprintf\s*\(([^)]*)\)/g,
    /\bvsprintf\s*\(([^)]*)\)/g,
    /\bscanf\s*\(\s*"%s"\s*,\s*([^)]+)\)/g,
    /\bfscanf\s*\([^,]+,\s*"%s"\s*,\s*([^)]+)\)/g,
    /\bsscanf\s*\([^,]+,\s*"%s"\s*,\s*([^)]+)\)/g,
  ];

  for (const regex of dangerousPatterns) {
    for (const match of code.matchAll(regex)) {
      if (match.index === undefined) continue;

      // strcpy/strcat with a string literal second arg is safe (no overflow risk)
      const fnName = match[0].match(/^\w+/)?.[0] ?? "";
      if (fnName === "strcpy" || fnName === "strcat") {
        const args = match[1]?.split(",") ?? [];
        const secondArg = args[1]?.trim() ?? "";
        if (/^"[^"]*"$/.test(secondArg) || /^L"[^"]*"$/.test(secondArg)) continue;
      }

      findings.push(
        createFinding({
          cweId: "CWE-787",
          ruleId: "out-of-bounds-write",
          vulnerability: "Out-of-bounds Write",
          severity: "high",
          message:
            "This code uses a function that can write past the bounds of a buffer. Consider safer bounded alternatives such as fgets, snprintf, or explicit length checks.",
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