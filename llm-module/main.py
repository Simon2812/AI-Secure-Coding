"""
Entry point for running secure coding experiments.

This script:
- initializes the evaluator
- configures experiment parameters
- runs the full pipeline (train + test)

Modify `training_overrides` to run different experiments.
"""

from experiment import run_experiment
from evaluator import Evaluator


if __name__ == "__main__":

    # Path to dataset metadata root
    metadata_root = "./dataset/metadata"

    # Evaluator instance (defines scoring logic)
    evaluator = Evaluator()

    # Run experiment with optional config overrides
    run_experiment(
        metadata_root=metadata_root,

        # Name used for checkpoint directory:
        # ./checkpoints/<experiment_name>
        experiment_name="baseline",

        # Override default training configuration
        training_overrides={
            "learning_rate": 2e-4,
            "lora_rank": 16,
            "epochs": 3,
        },

        evaluator=evaluator,
    )
