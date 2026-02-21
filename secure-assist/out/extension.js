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
let isTracking = false;
function activate(context) {
    const output = vscode.window.createOutputChannel("Secure Assist");
    // Command: Start Tracking
    const startCmd = vscode.commands.registerCommand("secure-assist.startTracking", () => {
        isTracking = true;
        output.show(true);
        output.appendLine("Tracking ON. Save any file to see events.");
        vscode.window.showInformationMessage("Secure Assist: tracking ON (save a file).");
    });
    // Listener: On Save
    const saveSub = vscode.workspace.onDidSaveTextDocument((doc) => {
        if (!isTracking)
            return; // only track after command is executed
        if (doc.isUntitled)
            return;
        if (doc.uri.scheme !== "file")
            return;
        const relPath = vscode.workspace.asRelativePath(doc.uri, false).replace(/\\/g, "/");
        const content = doc.getText();
        // safety limit: skip very large text
        const maxChars = 1_000_000;
        if (content.length > maxChars) {
            output.appendLine(`[SKIP] ${relPath} (too large: ${content.length} chars)`);
            return;
        }
        output.appendLine(`[SAVE] ${relPath} | chars=${content.length}`);
        // Later you’ll replace this with a real HTTP call
        // sendChange({ path: relPath, content, ts: Date.now() });
    });
    context.subscriptions.push(startCmd, saveSub, output);
}
function deactivate() { }
//# sourceMappingURL=extension.js.map