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
function walkJson(dir) {
    const results = [];
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory())
            results.push(...walkJson(fullPath));
        else if (entry.name.endsWith(".json"))
            results.push(fullPath);
    }
    return results;
}
function bucket(stats, cwe, isVuln, hasFindings) {
    if (!stats[cwe])
        stats[cwe] = { tp: 0, fn: 0, fp: 0, tn: 0 };
    if (isVuln && hasFindings)
        stats[cwe].tp++;
    else if (isVuln && !hasFindings)
        stats[cwe].fn++;
    else if (!isVuln && hasFindings)
        stats[cwe].fp++;
    else
        stats[cwe].tn++;
}
function totals(stats) {
    let tp = 0, fn = 0, fp = 0, tn = 0;
    for (const s of Object.values(stats)) {
        tp += s.tp;
        fn += s.fn;
        fp += s.fp;
        tn += s.tn;
    }
    return { tp, fn, fp, tn };
}
function pct(a, b) { return b > 0 ? (a / b * 100).toFixed(1) + "%" : "N/A"; }
async function main() {
    await (0, astAnalyzer_1.initAstAnalyzer)();
    const files = walkJson(METADATA_DIR);
    const regexStats = {};
    const astStats = {};
    for (const metaPath of files) {
        const meta = JSON.parse(fs.readFileSync(metaPath, "utf-8"));
        const codePath = path.join(REPO_ROOT, meta.path.replace(/^\//, ""));
        if (!fs.existsSync(codePath))
            continue;
        const code = fs.readFileSync(codePath, "utf-8");
        const isVuln = meta.vulnerabilities.length > 0;
        const rel = path.relative(METADATA_DIR, metaPath);
        const cwe = rel.split(path.sep)[0];
        const regexFindings = (0, analyze_1.analyzeCode)(code, codePath);
        const astFindings = (0, astAnalyzer_1.astAnalyzeCode)(code, codePath);
        bucket(regexStats, cwe, isVuln, regexFindings.length > 0);
        bucket(astStats, cwe, isVuln, astFindings.length > 0);
    }
    const pad = (s, n) => String(s).padStart(n);
    const lpad = (s, n) => s.padEnd(n);
    console.log("\n" + lpad("CWE", 15) +
        pad("Regex TP", 9) + pad("FN", 5) + pad("FP", 5) + pad("Det%", 7) + "  |" +
        pad("AST TP", 8) + pad("FN", 5) + pad("FP", 5) + pad("Det%", 7));
    console.log("-".repeat(70));
    const allCwes = new Set([...Object.keys(regexStats), ...Object.keys(astStats)]);
    for (const cwe of [...allCwes].sort()) {
        const r = regexStats[cwe] ?? { tp: 0, fn: 0, fp: 0, tn: 0 };
        const a = astStats[cwe] ?? { tp: 0, fn: 0, fp: 0, tn: 0 };
        const rv = r.tp + r.fn, av = a.tp + a.fn;
        console.log(lpad(cwe, 15) +
            pad(r.tp, 9) + pad(r.fn, 5) + pad(r.fp, 5) + pad(pct(r.tp, rv), 7) + "  |" +
            pad(a.tp, 8) + pad(a.fn, 5) + pad(a.fp, 5) + pad(pct(a.tp, av), 7));
    }
    const r = totals(regexStats), a = totals(astStats);
    const rv = r.tp + r.fn, av = a.tp + a.fn;
    const rs = r.fp + r.tn, as_ = a.fp + a.tn;
    console.log("-".repeat(70));
    console.log(lpad("TOTAL", 15) +
        pad(r.tp, 9) + pad(r.fn, 5) + pad(r.fp, 5) + pad(pct(r.tp, rv), 7) + "  |" +
        pad(a.tp, 8) + pad(a.fn, 5) + pad(a.fp, 5) + pad(pct(a.tp, av), 7));
    console.log(`\nRegex → Detection: ${pct(r.tp, rv)}  FP rate: ${pct(r.fp, rs)}`);
    console.log(`AST   → Detection: ${pct(a.tp, av)}  FP rate: ${pct(a.fp, as_)}`);
}
main().catch(e => { console.error(e); process.exit(1); });
//# sourceMappingURL=compareAnalyzers.js.map