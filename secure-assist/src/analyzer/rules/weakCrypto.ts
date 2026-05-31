import { RuleContext, Finding } from "../types";
import { createFinding } from "../utils";

export function findWeakCrypto(context: RuleContext): Finding[] {
  const findings: Finding[] = [];
  const { code, filePath, language } = context;

  let patterns: Array<{
    ruleId: string;
    cweId: string;
    vulnerability: string;
    severity: "medium";
    regex: RegExp;
    message: string;
  }> = [];

  if (language === "python") {
    patterns = [
      {
        ruleId: "python-md5",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /\bhashlib\.md5\s*\(/g,
        message: "hashlib.md5() uses MD5, which is considered cryptographically weak.",
      },
      {
        ruleId: "python-sha1",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /\bhashlib\.sha1\s*\(/g,
        message: "hashlib.sha1() uses SHA-1, which is considered cryptographically weak.",
      },
      {
        ruleId: "python-des",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /\b(Crypto\.Cipher\.DES|DES\.new)\b/g,
        message: "DES is an outdated and insecure encryption algorithm.",
      },
    ];
  } else if (language === "java") {
    patterns = [
      {
        ruleId: "java-md5",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /MessageDigest\s*\.\s*getInstance\s*\(\s*"MD5"\s*\)/g,
        message: 'MessageDigest.getInstance("MD5") uses MD5, which is considered cryptographically weak.',
      },
      {
        ruleId: "java-sha1",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /MessageDigest\s*\.\s*getInstance\s*\(\s*"SHA-?1"\s*\)/g,
        message: 'MessageDigest.getInstance("SHA-1") uses SHA-1, which is considered cryptographically weak.',
      },
      {
        ruleId: "java-des",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /Cipher\s*\.\s*getInstance\s*\(\s*"DES([\/"][^"]*)?"\s*\)/g,
        message: 'Cipher.getInstance("DES") uses DES, which is an outdated and insecure encryption algorithm.',
      },
    ];
  } else if (language === "cpp") {
    patterns = [
      {
        ruleId: "cpp-md5",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /\b(MD5\s*\(|EVP_md5\s*\()/g,
        message: "MD5 usage detected. MD5 is considered cryptographically weak.",
      },
      {
        ruleId: "cpp-sha1",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /\b(SHA1\s*\(|EVP_sha1\s*\()/g,
        message: "SHA-1 usage detected. SHA-1 is considered cryptographically weak.",
      },
      {
        ruleId: "cpp-des",
        cweId: "CWE-327",
        vulnerability: "Use of a Broken or Risky Cryptographic Algorithm",
        severity: "medium",
        regex: /\bDES_[A-Za-z0-9_]*\b/g,
        message: "DES usage detected. DES is an outdated and insecure encryption algorithm.",
      },
    ];
  }

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