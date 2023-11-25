import json
from typing import List, Dict

from loguru import logger
from pathlib import Path


class Catalog:
    def __init__(self, base_path: str = None):
        if base_path is None:
            # Set base_path to the parent directory of the directory where catalog.py is located
            base_path = Path(__file__).resolve().parent.parent
        self.base_path = base_path
        self.data_path = base_path / "data"
        self.figures_path = base_path / "figures"
        self.interaction_path = base_path / "owain_app"
        self.test_path = base_path / "tests"

    def _load_jsonl(self, filepath, notation_type):
        data = []
        with open(filepath, "r") as file:
            for line in file:
                item = json.loads(line)
                if notation_type == "set_notation":
                    item = set(item)  # Convert list back to set for set notation
                data.append(item)
        return data

    def _save_jsonl(self, data, filepath):
        try:
            with open(filepath, "w") as f:
                for item in data:
                    # Check if the item is a tuple (data, label)
                    if isinstance(item, tuple):
                        # Convert sets in the tuple to lists
                        item = tuple(
                            list(subitem) if isinstance(subitem, set) else subitem
                            for subitem in item
                        )
                    elif isinstance(item, set):
                        # Convert single set items to list
                        item = list(item)

                    json.dump(item, f)
                    f.write("\n")
            logger.info(f"Data successfully saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving data to {filepath}: {e}")

    def load_task(self, num_rules, rule_names, notation_type="set_notation"):
        dataset_name = "_and_".join(rule_names)
        dir_path = (
            self.data_path / "tasks" / f"n={num_rules}" / notation_type / dataset_name
        )

        train_file = dir_path / "train.jsonl"
        val_file = dir_path / "val.jsonl"
        test_file = dir_path / "test.jsonl"

        train_data = self._load_jsonl(train_file, notation_type)
        val_data = self._load_jsonl(val_file, notation_type)
        test_data = self._load_jsonl(test_file, notation_type)

        logger.info(f"Dataset loaded from {dir_path}")
        return {"train": train_data, "val": val_data, "test": test_data}

    def save_task(self, dataset, num_rules, dataset_name, notation_type="set_notation"):
        dir_path = (
            self.data_path / "tasks" / f"n={num_rules}" / notation_type / dataset_name
        )
        dir_path.mkdir(parents=True, exist_ok=True)

        train_file = dir_path / "train.jsonl"
        val_file = dir_path / "val.jsonl"
        test_file = dir_path / "test.jsonl"

        self._save_jsonl(dataset["train"], train_file)
        self._save_jsonl(dataset["val"], val_file)
        self._save_jsonl(dataset["test"], test_file)
        logger.info(f"Dataset for {dataset_name} saved in {dir_path}")

    def load_response(self, filename):
        response_file = self.interaction_path / filename
        with open(response_file, "r") as file:
            logger.info(f"Response loaded from {response_file}")
            return file.read()

    def save_response(self, response, filename):
        response_file = self.interaction_path / filename
        with open(response_file, "w") as file:
            file.write(response)
        logger.info(f"Response saved to {response_file}")

    def load_prompt(self, filepath):
        with open(filepath, "r") as file:
            return file.read()

    def save_response_interaction(self, response, filepath):
        full_path = self.base_path / filepath
        with open(full_path, "w") as file:
            file.write(response)
        logger.info(f"Response saved to {full_path}")
