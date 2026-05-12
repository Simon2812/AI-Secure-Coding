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
exports.CLang = exports.JavaLang = exports.PythonLang = void 0;
exports.initTreeSitter = initTreeSitter;
exports.newParser = newParser;
const path = __importStar(require("path"));
const web_tree_sitter_1 = require("web-tree-sitter");
let initialized = false;
async function initTreeSitter() {
    if (initialized)
        return;
    await web_tree_sitter_1.Parser.init({
        locateFile(scriptName) {
            return path.resolve(__dirname, "..", "..", "..", "node_modules", "web-tree-sitter", scriptName);
        },
    });
    const wasmBase = path.resolve(__dirname, "..", "..", "..", "node_modules");
    [exports.PythonLang, exports.JavaLang, exports.CLang] = await Promise.all([
        web_tree_sitter_1.Language.load(path.join(wasmBase, "tree-sitter-python", "tree-sitter-python.wasm")),
        web_tree_sitter_1.Language.load(path.join(wasmBase, "tree-sitter-java", "tree-sitter-java.wasm")),
        web_tree_sitter_1.Language.load(path.join(wasmBase, "tree-sitter-c", "tree-sitter-c.wasm")),
    ]);
    initialized = true;
}
function newParser() {
    return new web_tree_sitter_1.Parser();
}
//# sourceMappingURL=init.js.map