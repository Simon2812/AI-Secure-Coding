from pathlib import Path
import json
import random
import torch

from torch.optim import AdamW
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)
from peft import (
    LoraConfig,
    get_peft_model
)


class SecureCodingModel:
    """
    Secure coding LLM module.

    Responsibilities:
    - load quantized base model
    - attach LoRA adapters
    - load analyzer-enriched dataset
    - perform inference
    - fine-tune using supervised learning
    - validate through external evaluator
    - save and restore checkpoints
    """

    def __init__(self):
        """
        Initialize model identifiers,
        generation settings and training settings.
        """

        # Base instruction model.
        self.model_name = (
            "deepseek-ai/deepseek-coder-6.7b-instruct"
        )

        self.model = None
        self.tokenizer = None

        # Deterministic JSON generation.
        self.generation_config = {
            "temperature": 0.0,
            "do_sample": False,
            "max_new_tokens": 1024
        }

        # Initial training configuration.
        self.training_config = {
            "epochs": 3,
            "learning_rate": 2e-4
        }

        # Shared QLoRA quantization config.
        self.quantization_config = (
            BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=
                    torch.float16,
                bnb_4bit_use_double_quant=
                    True,
                bnb_4bit_quant_type=
                    "nf4"
            )
        )


    def load_model(self):
        """
        Load quantized base model
        and attach trainable LoRA adapters.
        """

        print(
            f"Loading model: "
            f"{self.model_name}"
        )

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                self.model_name
            )
        )

        # Some models do not define pad token.
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = (
                self.tokenizer.eos_token
            )

        self.model = (
            AutoModelForCausalLM
            .from_pretrained(
                self.model_name,
                device_map="auto",
                quantization_config=
                    self.quantization_config
            )
        )

        # LoRA enables lightweight fine-tuning.
        lora_config = LoraConfig(
            r=16,
            lora_alpha=32,
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )

        self.model = get_peft_model(
            self.model,
            lora_config
        )

        self.model.print_trainable_parameters()

        print(
            "Model loaded successfully."
        )


    def load_dataset(self, metadata_root):
        """
        Load metadata files, resolve source code,
        and split samples into train/val/test.
        """

        train_data = []
        val_data = []
        test_data = []

        metadata_root = Path(metadata_root)

        for json_file in metadata_root.rglob("*.json"):

            with open(
                json_file,
                "r",
                encoding="utf-8"
            ) as file:
                metadata = json.load(file)

            # Source code path is stored inside metadata.
            code_path = Path(
                metadata["path"].lstrip("/")
            )

            with open(
                code_path,
                "r",
                encoding="utf-8"
            ) as file:
                code = file.read()

            sample = {
                "code": code,
                "analysis": metadata["analysis"],
                "target": metadata["vulnerabilities"],
                "split": metadata["split"],
                "language": metadata["language"],
                "metadata": metadata
            }

            split = metadata["split"]

            if split == "train":
                train_data.append(sample)

            elif split == "val":
                val_data.append(sample)

            elif split == "test":
                test_data.append(sample)

            else:
                raise ValueError(
                    f"Unknown split: {split}"
                )

        print(
            f"Loaded "
            f"{len(train_data)} train, "
            f"{len(val_data)} val, "
            f"{len(test_data)} test samples."
        )

        return train_data, val_data, test_data


    def save_checkpoint(self, checkpoint_dir):
        """
        Save current LoRA weights,
        tokenizer and training config.
        """

        checkpoint_path = Path(
            checkpoint_dir
        )

        checkpoint_path.mkdir(
            parents=True,
            exist_ok=True
        )

        print(
            f"Saving checkpoint to "
            f"{checkpoint_path}"
        )

        if self.model is None:
            raise RuntimeError(
                "Cannot save checkpoint before model is loaded."
            )

        self.model.save_pretrained(
            checkpoint_path
        )

        self.tokenizer.save_pretrained(
            checkpoint_path
        )

        config_path = (
            checkpoint_path
            / "training_config.json"
        )

        with open(
            config_path,
            "w"
        ) as file:

            json.dump(
                self.training_config,
                file,
                indent=4
            )

        print("Checkpoint saved.")


    def load_checkpoint(self, checkpoint_dir):
        """
        Restore trained LoRA adapters
        from an existing checkpoint.
        """

        checkpoint_path = Path(
            checkpoint_dir
        )

        if not checkpoint_path.exists():
            raise FileNotFoundError(
                f"Checkpoint not found: "
                f"{checkpoint_path}"
            )

        print(
            f"Loading checkpoint from "
            f"{checkpoint_path}"
        )

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                checkpoint_path
            )
        )

        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = (
                self.tokenizer.eos_token
            )

        # Recreate quantized base model.
        base_model = (
            AutoModelForCausalLM
            .from_pretrained(
                self.model_name,
                device_map="auto",
                quantization_config=
                    self.quantization_config
            )
        )

        from peft import PeftModel

        self.model = (
            PeftModel.from_pretrained(
                base_model,
                checkpoint_path
            )
        )

        self.model.print_trainable_parameters()

        print(
            "Checkpoint loaded."
        )


    def build_input(self, code, analysis):
        """
        Build unified prompt used for:
        - training
        - validation
        - inference
        """

        prompt = f"""
        You are a secure coding assistant.

        Analyze the provided source code together with static analyzer findings.

        Identify vulnerabilities and suggest exact minimal fixes.

        Source Code:
        {code}

        Static Analyzer Findings:
        {json.dumps(analysis, indent=2)}

        Return ONLY valid JSON
        with the following schema:

        {{
        "vulnerabilities": [
            {{
            "cwe": "...",
            "fixes": [
                {{
                "origin": "...",
                "replacement": "..."
                }}
            ]
            }}
        ]
        }}
        """

        return prompt.strip()


    def predict(self, code, analysis):
        """
        Generate structured vulnerability
        prediction for one code sample.
        """

        if self.model is None:
            raise RuntimeError(
                "Model must be loaded."
            )

        input_text = self.build_input(
            code,
            analysis
        )

        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            truncation=True,
            max_length=2048
        )

        # Align tensors with model device.
        device = next(
            self.model.parameters()
        ).device

        inputs = {
            key: value.to(device)
            for key, value in inputs.items()
        }

        outputs = self.model.generate(
            **inputs,
            **self.generation_config
        )

        generated_text = (
            self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )
        )

        return self.extract_json(
            generated_text
        )


    def train(self, train_data, val_data, evaluator):
        """
        Fine-tune LoRA adapters on train split.

        Validation is performed after each epoch.
        Best checkpoint is selected using evaluator.
        """

        if self.model is None:
            raise RuntimeError(
                "Model must be loaded."
            )

        epochs = (
            self.training_config[
                "epochs"
            ]
        )

        best_validation_score = -1

        # Only train LoRA parameters.
        optimizer = AdamW(
            filter(
                lambda p: p.requires_grad,
                self.model.parameters()
            ),
            lr=self.training_config[
                "learning_rate"
            ]
        )

        for epoch in range(epochs):

            print(
                f"\nEpoch "
                f"{epoch + 1}/{epochs}"
            )

            self.model.train()

            # Shuffle train samples every epoch.
            random.shuffle(
                train_data
            )

            total_loss = 0

            for sample in train_data:

                prompt = self.build_input(
                    sample["code"],
                    sample["analysis"]
                )

                target = (
                    sample["target"]
                )

                full_text = (
                    prompt
                    + "\n"
                    + json.dumps(
                        target,
                        indent=2
                    )
                )

                inputs = self.tokenizer(
                    full_text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=2048
                )

                device = next(
                    self.model.parameters()
                ).device

                inputs = {
                    key: value.to(device)
                    for key, value in inputs.items()
                }

                optimizer.zero_grad()

                outputs = self.model(
                    **inputs,
                    labels=inputs[
                        "input_ids"
                    ]
                )

                loss = outputs.loss

                total_loss += (
                    loss.item()
                )

                loss.backward()

                optimizer.step()

            average_loss = (
                total_loss
                / len(train_data)
            )

            print(
                f"Train loss: "
                f"{average_loss:.4f}"
            )

            self.model.eval()

            validation_score = 0

            # Validation never updates weights.
            with torch.no_grad():

                for sample in val_data:

                    prediction = (
                        self.predict(
                            sample["code"],
                            sample["analysis"]
                        )
                    )

                    score = (
                        evaluator.evaluate(
                            sample,
                            prediction
                        )
                    )

                    validation_score += score

            validation_score /= len(
                val_data
            )

            print(
                f"Validation score: "
                f"{validation_score:.4f}"
            )

            # Keep only best checkpoint.
            if (
                validation_score
                > best_validation_score
            ):

                best_validation_score = (
                    validation_score
                )

                self.save_checkpoint(
                    "./checkpoints/best"
                )

                print(
                    "New best checkpoint."
                )

        print(
            "\nTraining completed."
        )


    def extract_json(self, text):
        """
        Extract first JSON object
        from generated model output.
        """

        start = text.find("{")
        end = text.rfind("}")

        if start == -1 or end == -1:
            raise ValueError(
                "No JSON found."
            )

        json_text = text[
            start:end + 1
        ]

        return json.loads(
            json_text
        )
