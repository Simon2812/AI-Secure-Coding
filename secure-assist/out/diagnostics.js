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
exports.createDiagnosticCollection = createDiagnosticCollection;
exports.updateDiagnostics = updateDiagnostics;
const vscode = __importStar(require("vscode"));
function createDiagnosticCollection() {
    return vscode.languages.createDiagnosticCollection("secure-assist");
}
function updateDiagnostics(collection, doc, findings) {
    const diagnostics = findings.map((finding) => {
        const line = Math.max(0, finding.line - 1);
        const col = Math.max(0, finding.column - 1);
        const start = new vscode.Position(line, col);
        const end = new vscode.Position(line, col + Math.max(1, finding.evidence.length));
        const range = new vscode.Range(start, end);
        const diagnostic = new vscode.Diagnostic(range, `[${finding.cweId}] ${finding.message}`, mapSeverity(finding.severity));
        diagnostic.source = "Secure Assist";
        diagnostic.code = finding.ruleId;
        return diagnostic;
    });
    collection.set(doc.uri, diagnostics);
}
function mapSeverity(severity) {
    switch (severity) {
        case "high":
            return vscode.DiagnosticSeverity.Error;
        case "medium":
            return vscode.DiagnosticSeverity.Warning;
        case "low":
            return vscode.DiagnosticSeverity.Information;
        default:
            return vscode.DiagnosticSeverity.Warning;
    }
}
//# sourceMappingURL=diagnostics.js.map