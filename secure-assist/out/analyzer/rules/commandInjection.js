"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.findCommandInjection = findCommandInjection;
const utils_1 = require("../utils");
function findCommandInjection(context) {
    const findings = [];
    const { code, filePath, language } = context;
    let patterns = [];
    if (language === "cpp") {
        patterns = [
            {
                ruleId: "cpp-system",
                cweId: "CWE-78",
                vulnerability: "OS Command Injection",
                severity: "high",
                regex: /\bsystem\s*\(/g,
                message: "Use of system() may allow OS command injection if input is not controlled.",
            },
            {
                ruleId: "cpp-popen",
                cweId: "CWE-78",
                vulnerability: "OS Command Injection",
                severity: "high",
                regex: /\bpopen\s*\(/g,
                message: "Use of popen() may allow OS command injection if input is not controlled.",
            },
        ];
    }
    else if (language === "java") {
        patterns = [
            {
                ruleId: "java-runtime-exec",
                cweId: "CWE-78",
                vulnerability: "OS Command Injection",
                severity: "high",
                regex: /Runtime\s*\.\s*getRuntime\s*\(\s*\)\s*\.\s*exec\s*\(/g,
                message: "Runtime.getRuntime().exec() may allow OS command injection if input is not controlled.",
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
    }
    else if (language === "python") {
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
            if (match.index === undefined)
                continue;
            findings.push((0, utils_1.createFinding)({
                cweId: pattern.cweId,
                ruleId: pattern.ruleId,
                vulnerability: pattern.vulnerability,
                severity: pattern.severity,
                message: pattern.message,
                file: filePath,
                code,
                index: match.index,
                evidence: match[0],
            }));
        }
    }
    return findings;
}
//# sourceMappingURL=commandInjection.js.map