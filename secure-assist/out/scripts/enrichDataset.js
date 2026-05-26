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
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const analyze_1 = require("../analyzer/analyze");
const astAnalyzer_1 = require("./ast/astAnalyzer");
const REPO_ROOT = process.argv[2]
    ? path.resolve(process.argv[2])
    : path.resolve(__dirname, "..", "..", "..");
const METADATA_DIR = path.join(REPO_ROOT, "dataset", "metadata");
const SECURE_ASSIST_ROOT = path.resolve(__dirname, "..", "..");
const ENRICHED_DIR = path.join(SECURE_ASSIST_ROOT, "enriched");
// CWEs where AST outperforms regex
const AST_STRONG = new Set(["CWE-22", "CWE-78", "CWE-89", "CWE-190", "CWE-259", "CWE-321", "CWE-327", "CWE-328", "CWE-416", "CWE-787", "MULTI-CWE"]);
function pickAnalyzer(metaPath, code, codePath) {
    const cweFolder = path.relative(METADATA_DIR, metaPath).split(path.sep)[0];
    if (AST_STRONG.has(cweFolder)) {
        return (0, astAnalyzer_1.astAnalyzeCode)(code, codePath);
    }
    return (0, analyze_1.analyzeCode)(code, codePath);
}
function walkJson(dir) {
    const results = [];
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            results.push(...walkJson(fullPath));
        }
        else if (entry.isFile() && entry.name.endsWith(".json")) {
            results.push(fullPath);
        }
    }
    return results;
}
async function main() {
    await (0, astAnalyzer_1.initAstAnalyzer)();
    const metadataFiles = walkJson(METADATA_DIR);
    let processed = 0;
    let skipped = 0;
    let errors = 0;
    console.log(`Found ${metadataFiles.length} metadata files.\n`);
    for (const metaPath of metadataFiles) {
        let meta;
        try {
            meta = JSON.parse(fs.readFileSync(metaPath, "utf-8"));
        }
        catch (e) {
            console.error(`[ERROR] Failed to parse ${metaPath}: ${e}`);
            errors++;
            continue;
        }
        const codePath = path.join(REPO_ROOT, meta.path.replace(/^\//, ""));
        if (!fs.existsSync(codePath)) {
            console.warn(`[SKIP] Code file not found: ${codePath}`);
            skipped++;
            continue;
        }
        const code = fs.readFileSync(codePath, "utf-8");
        const findings = pickAnalyzer(metaPath, code, codePath);
        const enriched = {
            ...meta,
            static_findings: findings,
            enriched_at: new Date().toISOString(),
        };
        const relPath = path.relative(METADATA_DIR, metaPath);
        const outPath = path.join(ENRICHED_DIR, relPath);
        fs.mkdirSync(path.dirname(outPath), { recursive: true });
        fs.writeFileSync(outPath, JSON.stringify(enriched, null, 2), "utf-8");
        console.log(`[OK] ${meta.id} → ${findings.length} finding(s)`);
        processed++;
    }
    console.log(`\nDone. Processed: ${processed}, Skipped: ${skipped}, Errors: ${errors}`);
}
main().catch(err => { console.error(err); process.exit(1); });
//# sourceMappingURL=enrichDataset.js.map