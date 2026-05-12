import * as fs from "fs";
import * as path from "path";
import { analyzeCode } from "../analyzer/analyze";
import { Finding } from "../analyzer/types";

const REPO_ROOT = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.resolve(__dirname, "..", "..", "..");
const METADATA_DIR = path.join(REPO_ROOT, "dataset", "metadata");
const SECURE_ASSIST_ROOT = path.resolve(__dirname, "..", "..");
const ENRICHED_DIR = path.join(SECURE_ASSIST_ROOT, "enriched");

interface Vulnerability {
  id: string;
  cwe: string;
  fixes: Array<{ origin: string; replacement: string }>;
}

interface Metadata {
  schema_version: string;
  id: string;
  language: string;
  path: string;
  split: string;
  source: { type: string; name: string | null };
  vulnerabilities: Vulnerability[];
}

interface EnrichedMetadata extends Metadata {
  static_findings: Finding[];
  enriched_at: string;
}

function walkJson(dir: string): string[] {
  const results: string[] = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      results.push(...walkJson(fullPath));
    } else if (entry.isFile() && entry.name.endsWith(".json")) {
      results.push(fullPath);
    }
  }
  return results;
}

function main() {
  const metadataFiles = walkJson(METADATA_DIR);

  let processed = 0;
  let skipped = 0;
  let errors = 0;

  console.log(`Found ${metadataFiles.length} metadata files.\n`);

  for (const metaPath of metadataFiles) {
    let meta: Metadata;

    try {
      meta = JSON.parse(fs.readFileSync(metaPath, "utf-8")) as Metadata;
    } catch (e) {
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
    const findings = analyzeCode(code, codePath);

    const enriched: EnrichedMetadata = {
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

main();
