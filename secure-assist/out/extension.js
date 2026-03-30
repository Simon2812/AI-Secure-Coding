"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = __importStar(require("vscode"));
const analyze_1 = require("./analyzer/analyze");
let isTracking = false;
const fileStore = new Map();
function activate(context) {
    const output = vscode.window.createOutputChannel("Secure Assist");
    const startCmd = vscode.commands.registerCommand("secure-assist.startTracking", () => {
        isTracking = true;
        output.show(true);
        output.appendLine("Tracking ON. Save any file to analyze it.");
        vscode.window.showInformationMessage("Secure Assist: tracking ON.");
    });
    const showStoredCmd = vscode.commands.registerCommand("secure-assist.showStoredFile", async () => {
        if (fileStore.size === 0) {
            vscode.window.showWarningMessage("Secure Assist: no stored files yet.");
            return;
        }
        const picked = await vscode.window.showQuickPick([...fileStore.keys()].sort(), {
            placeHolder: "Select a stored file to view",
        });
        if (!picked)
            return;
        const content = fileStore.get(picked) ?? "";
        const doc = await vscode.workspace.openTextDocument({
            content,
            language: guessLanguageFromPath(picked),
        });
        await vscode.window.showTextDocument(doc, { preview: true });
    });
    const saveSub = vscode.workspace.onDidSaveTextDocument((doc) => {
        if (!isTracking)
            return;
        if (doc.isUntitled)
            return;
        if (doc.uri.scheme !== "file")
            return;
        const relPath = vscode.workspace.asRelativePath(doc.uri, false).replace(/\\/g, "/");
        const content = doc.getText();
        const maxChars = 1_000_000;
        if (content.length > maxChars) {
            output.appendLine(`[SKIP] ${relPath} (too large: ${content.length} chars)`);
            return;
        }
        fileStore.set(relPath, content);
        output.appendLine(``);
        output.appendLine(`=== Analyzing ${relPath} ===`);
        const findings = (0, analyze_1.analyzeCode)(content, relPath);
        if (findings.length === 0) {
            output.appendLine(`No findings.`);
            return;
        }
        printFindings(output, findings);
    });
    context.subscriptions.push(startCmd, showStoredCmd, saveSub, output);
}
function deactivate() { }
function printFindings(output, findings) {
    for (const finding of findings) {
        output.appendLine(`[${finding.severity.toUpperCase()}] ${finding.cweId} | ${finding.ruleId}`);
        output.appendLine(`File: ${finding.file}:${finding.line}:${finding.column}`);
        output.appendLine(`Issue: ${finding.vulnerability}`);
        output.appendLine(`Message: ${finding.message}`);
        output.appendLine(`Evidence: ${finding.evidence}`);
        output.appendLine(`---`);
    }
}
function guessLanguageFromPath(path) {
    const lower = path.toLowerCase();
    if (lower.endsWith(".ts"))
        return "typescript";
    if (lower.endsWith(".tsx"))
        return "typescriptreact";
    if (lower.endsWith(".js"))
        return "javascript";
    if (lower.endsWith(".jsx"))
        return "javascriptreact";
    if (lower.endsWith(".json"))
        return "json";
    if (lower.endsWith(".py"))
        return "python";
    if (lower.endsWith(".c"))
        return "c";
    if (lower.endsWith(".cpp"))
        return "cpp";
    if (lower.endsWith(".h"))
        return "c";
    if (lower.endsWith(".java"))
        return "java";
    if (lower.endsWith(".cs"))
        return "csharp";
    if (lower.endsWith(".html"))
        return "html";
    if (lower.endsWith(".css"))
        return "css";
    if (lower.endsWith(".md"))
        return "markdown";
    return "plaintext";
}
//# sourceMappingURL=extension.js.map