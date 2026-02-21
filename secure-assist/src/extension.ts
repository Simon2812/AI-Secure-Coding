import * as vscode from "vscode";

let isTracking = false;

export function activate(context: vscode.ExtensionContext) {
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
    if (!isTracking) return; // only track after command is executed
    if (doc.isUntitled) return;
    if (doc.uri.scheme !== "file") return;

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

export function deactivate() {}