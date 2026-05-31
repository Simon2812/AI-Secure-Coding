import json
import subprocess
import tempfile

from pathlib import Path
from collections import Counter


class Evaluator:
    """
    Secure coding evaluator.

    Responsibilities:
    - compare predicted and ground-truth CWEs
    - apply predicted fixes
    - validate fixes through compilation
    - validate fixes through analyzer reruns
    - compute final evaluation scores
    """

    def __init__(self):
        """
        Initialize evaluator paths
        and language configuration.
        """

        # Assumes repository layout:
        # repo/
        # ├── secure-assist/
        # └── llm-module/
        self.project_root = (
            Path(__file__).resolve().parent.parent
            / "secure-assist"
        ).resolve()

        self.analyzer_runner = (
            self.project_root
            / "src"
            / "analyzer"
            / "analyzer_runner.ts"
        )

        if not self.analyzer_runner.exists():
            raise RuntimeError(
                f"Analyzer runner not found: {self.analyzer_runner}"
            )

        self.language_suffix = {
            "c": ".c",
            "python": ".py",
            "java": ".java",
        }


    def evaluate(self, sample, prediction):
        """
        Evaluate a single prediction.

        Returns:
            dict with keys:
                - final_score
                - cwe_score
                - fix_score
        """

        pred_vulns = self._get_predicted_vulns(
            prediction
        )

        gt_cwes = set(
            sample["cwes"]
        )

        pred_cwes = self._extract_predicted_cwes(
            pred_vulns
        )

        cwe_score = self._f1_score(
            gt_cwes,
            pred_cwes,
        )

        # Safe sample case.
        if not gt_cwes:
            fix_score = (
                1.0
                if not pred_cwes
                else 0.0
            )

            return {
                "final_score": (
                    0.5 * cwe_score +
                    0.5 * fix_score
                ),
                "cwe_score": cwe_score,
                "fix_score": fix_score,
            }

        patched_code = self._apply_fixes(
            code=sample["code"],
            pred_vulns=pred_vulns,
            gt_cwes=gt_cwes,
        )

        analyzer_score, introduced_findings = (
            self._analyze_reduction(
                patched_code=patched_code,
                sample=sample,
            )
        )

        introduced_penalty = min(
            0.8,
            0.05 * introduced_findings,
        )

        if sample["language"] == "java":
            fix_score = (
                analyzer_score -
                introduced_penalty
            )

        else:
            compile_score = self._compile_code(
                code=patched_code,
                language=sample["language"],
            )

            fix_score = (
                0.8 * analyzer_score +
                0.2 * compile_score -
                introduced_penalty
            )

        fix_score = max(
            0.0,
            min(1.0, fix_score),
        )

        final_score = (
            0.5 * cwe_score +
            0.5 * fix_score
        )

        return {
            "final_score": final_score,
            "cwe_score": cwe_score,
            "fix_score": fix_score,
        }


    def _get_predicted_vulns(self, prediction):
        """
        Safely extract vulnerability list
        from model prediction.
        """

        if not isinstance(prediction, dict):
            return []

        pred_vulns = prediction.get(
            "vulnerabilities",
            [],
        )

        if not isinstance(pred_vulns, list):
            return []

        return pred_vulns


    def _extract_predicted_cwes(self, pred_vulns):
        """
        Extract CWE IDs from prediction.
        """

        return {
            vuln.get("cwe")
            for vuln in pred_vulns
            if isinstance(vuln, dict)
            and isinstance(vuln.get("cwe"), str)
        }


    def _f1_score(self, gt_cwes, pred_cwes):
        """
        Compute F1 score between
        ground-truth and predicted CWEs.
        """

        if not gt_cwes and not pred_cwes:
            return 1.0

        if not gt_cwes or not pred_cwes:
            return 0.0

        tp = len(
            gt_cwes &
            pred_cwes
        )

        fp = len(
            pred_cwes -
            gt_cwes
        )

        fn = len(
            gt_cwes -
            pred_cwes
        )

        precision = (
            tp / (tp + fp)
            if (tp + fp) > 0
            else 0.0
        )

        recall = (
            tp / (tp + fn)
            if (tp + fn) > 0
            else 0.0
        )

        if precision + recall == 0:
            return 0.0

        return (
            2 *
            precision *
            recall /
            (precision + recall)
        )


    def _apply_fixes(
        self,
        code,
        pred_vulns,
        gt_cwes,
    ):
        """
        Apply predicted fixes to source code.

        Only fixes associated with
        ground-truth CWEs are applied.
        """

        patched_code = code

        for vuln in pred_vulns:
            if not isinstance(vuln, dict):
                continue

            cwe = vuln.get("cwe")

            if cwe not in gt_cwes:
                continue

            fixes = vuln.get(
                "fixes",
                [],
            )

            if not isinstance(fixes, list):
                continue

            for fix in fixes:
                if not isinstance(fix, dict):
                    continue

                origin = fix.get("origin")
                replacement = fix.get("replacement")

                if not isinstance(origin, str):
                    continue

                if not isinstance(replacement, str):
                    continue

                if origin in patched_code:
                    patched_code = patched_code.replace(
                        origin,
                        replacement,
                        1,
                    )

        return patched_code


    def _compile_code(self, code, language):
        """
        Compile or syntax-check patched code.

        Java compilation is skipped by design.
        Java fix scoring uses analyzer reduction only.
        """

        suffix = self.language_suffix.get(
            language
        )

        if suffix is None:
            return 0.0

        if language == "java":
            return 0.0

        with tempfile.TemporaryDirectory() as tmp:
            source_file = Path(tmp) / f"patched{suffix}"

            source_file.write_text(
                code,
                encoding="utf-8",
            )

            try:
                if language == "python":
                    command = [
                        "python",
                        "-m",
                        "py_compile",
                        str(source_file),
                    ]

                elif language == "c":
                    command = [
                        "gcc",
                        "-fsyntax-only",
                        str(source_file),
                    ]

                else:
                    return 0.0

                result = subprocess.run(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=10,
                )

                return (
                    1.0
                    if result.returncode == 0
                    else 0.0
                )

            except Exception:
                return 0.0


    def _analyze_reduction(
        self,
        patched_code,
        sample,
    ):
        """
        Run analyzer on patched code and measure
        reduction of supported CWE findings.

        Returns:
            (
                analyzer_score,
                introduced_findings,
            )
        """

        gt_cwes = set(
            sample["cwes"]
        )

        original_findings = sample.get(
            "static_findings",
            [],
        )

        supported_original_counts = Counter()

        for finding in original_findings:
            if not isinstance(finding, dict):
                continue

            cwe = finding.get("cweId")

            if cwe in gt_cwes:
                supported_original_counts[cwe] += 1

        original_total = sum(
            supported_original_counts.values()
        )

        if original_total == 0:
            return 0.0, 0

        new_findings = self._run_analyzer(
            code=patched_code,
            language=sample["language"],
        )

        new_supported_total = 0

        for finding in new_findings:
            if not isinstance(finding, dict):
                continue

            cwe = finding.get("cweId")

            if cwe in supported_original_counts:
                new_supported_total += 1

        removed = max(
            0,
            original_total - new_supported_total,
        )

        analyzer_score = (
            removed /
            original_total
        )

        introduced_findings = self._count_introduced_findings(
            original_findings=original_findings,
            new_findings=new_findings,
        )

        return analyzer_score, introduced_findings


    def _count_introduced_findings(
        self,
        original_findings,
        new_findings,
    ):
        """
        Count findings introduced after patching.

        Counting is based on CWE frequency,
        not exact line numbers, because line
        numbers may change after fixes.
        """

        original_counts = self._count_findings_by_cwe(
            original_findings
        )

        new_counts = self._count_findings_by_cwe(
            new_findings
        )

        introduced = 0

        for cwe, new_count in new_counts.items():
            old_count = original_counts.get(
                cwe,
                0,
            )

            if new_count > old_count:
                introduced += (
                    new_count -
                    old_count
                )

        return introduced


    def _count_findings_by_cwe(self, findings):
        """
        Count analyzer findings by CWE ID.
        """

        counts = Counter()

        for finding in findings:
            if not isinstance(finding, dict):
                continue

            cwe = finding.get("cweId")

            if isinstance(cwe, str):
                counts[cwe] += 1

        return counts


    def _run_analyzer(self, code, language):
        """
        Run TypeScript analyzer through
        analyzer_runner.ts.
        """

        suffix = self.language_suffix.get(
            language
        )

        if suffix is None:
            raise RuntimeError(
                f"Unsupported language for analyzer: {language}"
            )

        with tempfile.TemporaryDirectory() as tmp:
            source_file = Path(tmp) / f"patched{suffix}"

            source_file.write_text(
                code,
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    "npx",
                    "ts-node",
                    str(self.analyzer_runner),
                    str(source_file),
                ],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=20,
            )

            if result.returncode != 0:
                raise RuntimeError(
                    "Analyzer execution failed.\n"
                    f"STDOUT:\n{result.stdout}\n"
                    f"STDERR:\n{result.stderr}"
                )

            try:
                findings = json.loads(
                    result.stdout
                )

            except json.JSONDecodeError as error:
                raise RuntimeError(
                    "Analyzer returned invalid JSON.\n"
                    f"Output:\n{result.stdout}"
                ) from error

            if not isinstance(findings, list):
                raise RuntimeError(
                    "Analyzer output must be a JSON list."
                )

            return findings
