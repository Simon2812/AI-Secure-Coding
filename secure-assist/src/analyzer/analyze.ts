import { Finding, RuleContext } from "./types";
import { detectLanguage } from "./utils";
import { findHardcodedCredentials } from "./rules/hardcodedCredentials";
import { findWeakCrypto } from "./rules/weakCrypto";
import { findCommandInjection } from "./rules/commandInjection";
import { findSqlInjection } from "./rules/sqlInjection";
import { findPathTraversal } from "./rules/pathTraversal";

export function analyzeCode(code: string, filePath: string): Finding[] {
  const context: RuleContext = {
    code,
    filePath,
    language: detectLanguage(filePath),
  };

  const findings: Finding[] = [];

  findings.push(...findHardcodedCredentials(context));
  findings.push(...findWeakCrypto(context));
  findings.push(...findCommandInjection(context));
  findings.push(...findSqlInjection(context));
  findings.push(...findPathTraversal(context));
  


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