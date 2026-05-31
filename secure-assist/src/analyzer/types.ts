export type Severity = "low" | "medium" | "high";

export type Finding = {
  cweId: string;
  ruleId: string;
  vulnerability: string;
  severity: Severity;
  message: string;
  file: string;
  line: number;
  column: number;
  evidence: string;
};

export type RuleContext = {
  code: string;
  filePath: string;
  language: string;
};

export type Rule = (context: RuleContext) => Finding[];