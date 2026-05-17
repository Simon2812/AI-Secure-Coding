class Evaluator:
    """
    Evaluator for secure coding model outputs.

    Responsibilities:
    - compare model predictions with ground truth
    - compute scores (final, CWE, fix)
    """

    def __init__(self):
        """
        Initialize evaluator state if needed.
        """
        pass


    def evaluate(self, sample, prediction):
        """
        Evaluate a single sample.

        Args:
            sample (dict): Ground truth sample containing:
                - target (vulnerabilities)
                - cwes
                - other metadata

            prediction (dict): Model output JSON

        Returns:
            dict with keys:
                - final_score (float)
                - cwe_score (float)
                - fix_score (float)
        """

        raise NotImplementedError(
            "Evaluator.evaluate() is not implemented yet."
        )
