import { Finding } from "./types";
import { findHardcodedCredentials } from "./rules/hardcodedCredentials";
// import { findWeakCrypto } from "./rules/weakCrypto";
// import { findCommandInjection } from "./rules/commandInjection";

export function analyzeCode(code: string, filePath: string): Finding[] {
  const findings: Finding[] = [];

  findings.push(...findHardcodedCredentials({ code, filePath }));
//   findings.push(...findWeakCrypto({ code, filePath }));
//   findings.push(...findCommandInjection({ code, filePath }));

  return sortFindings(findings);
}

function sortFindings(findings: Finding[]): Finding[] {
  const severityOrder = {
    high: 0,
    medium: 1,
    low: 2,
  };

  return findings.sort((a, b) => {
    const sevDiff = severityOrder[a.severity] - severityOrder[b.severity];
    if (sevDiff !== 0) return sevDiff;

    if (a.line !== b.line) return a.line - b.line;
    return a.column - b.column;
  });
}