// Run: node test-samples/run-tests.js   (from secure-assist root, after `npm run compile`)
"use strict";

const path = require("path");
const fs = require("fs");

const OUT = path.resolve(__dirname, "../out");
const { initAstAnalyzer, astAnalyzeCode } = require(path.join(OUT, "scripts/ast/astAnalyzer"));

// Expected CWE tag per directory — used only for pass/fail display
const CWE_MAP = {
  "CWE-22":  "CWE-22",
  "CWE-78":  "CWE-78",
  "CWE-89":  "CWE-89",
  "CWE-190": "CWE-190",
  "CWE-259": "CWE-259",
  "CWE-321": "CWE-321",
  "CWE-327": "CWE-327",
  "CWE-328": "CWE-328",
  "CWE-416": "CWE-416",
  "CWE-787": "CWE-787",
};

function collectSamples() {
  const samples = [];
  const samplesDir = __dirname;
  for (const cweDir of fs.readdirSync(samplesDir)) {
    const full = path.join(samplesDir, cweDir);
    if (!fs.statSync(full).isDirectory()) continue;
    if (!CWE_MAP[cweDir]) continue;
    for (const f of fs.readdirSync(full)) {
      if (!f.startsWith("sample-")) continue;
      samples.push({ cwe: cweDir, file: path.join(full, f) });
    }
  }
  return samples.sort((a, b) => a.file.localeCompare(b.file));
}

async function main() {
  await initAstAnalyzer();

  const samples = collectSamples();

  const results = [];
  for (const { cwe, file } of samples) {
    const code = fs.readFileSync(file, "utf8");
    const findings = astAnalyzeCode(code, file);
    const hit = findings.some(f => (f.cweId || f.cwe) === cwe);
    const relFile = path.relative(path.dirname(__dirname), file).replace(/\\/g, "/");
    results.push({ cwe, file: relFile, hit, findings });
  }

  // --- Summary table ---
  const CWE_ORDER = Object.keys(CWE_MAP);
  const grouped = {};
  for (const r of results) {
    if (!grouped[r.cwe]) grouped[r.cwe] = [];
    grouped[r.cwe].push(r);
  }

  let totalPass = 0, totalFail = 0;

  console.log("\n=== Test Sample Results ===\n");
  console.log(
    "CWE      File                              Detected  Findings"
  );
  console.log("─".repeat(80));

  for (const cwe of CWE_ORDER) {
    const group = grouped[cwe] || [];
    for (const r of group) {
      const fname = path.basename(r.file);
      const status = r.hit ? "✓ YES " : "✗ NO  ";
      const tags = [...new Set(r.findings.map(f => f.cweId || f.cwe))].join(", ") || "(none)";
      console.log(`${cwe.padEnd(8)} ${fname.padEnd(33)} ${status}    ${tags}`);
      if (r.hit) totalPass++; else totalFail++;
    }
    if (group.length) console.log();
  }

  const total = totalPass + totalFail;
  console.log("─".repeat(80));
  console.log(`TOTAL: ${totalPass}/${total} detected  (${((totalPass/total)*100).toFixed(1)}%)\n`);

  // --- Per-CWE detection rate ---
  console.log("Per-CWE detection rate:");
  for (const cwe of CWE_ORDER) {
    const group = grouped[cwe] || [];
    if (!group.length) continue;
    const pass = group.filter(r => r.hit).length;
    console.log(`  ${cwe}: ${pass}/${group.length}`);
  }
  console.log();

  // --- Missed files ---
  const missed = results.filter(r => !r.hit);
  if (missed.length) {
    console.log("Missed (not detected):");
    for (const r of missed) {
      const otherTags = [...new Set(r.findings.map(f => f.cweId || f.cwe))].join(", ") || "(none)";
      console.log(`  ${r.cwe}  ${path.basename(r.file)}  → found: ${otherTags}`);
    }
    console.log();
  }
}

main().catch(err => { console.error(err); process.exit(1); });
