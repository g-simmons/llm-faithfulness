import json
from typing import List, Union, Optional
from owain_app.schemas import Task, ICLPrompt

from loguru import logger
from pathlib import Path
from pydantic import BaseModel


def iter_validate(iterable, validator):
    for item in iterable:
        try:
            validator(item)
        except Exception as e:
            print(validator)
            print(item)
            print(e)
            print("Validation failed")


class Catalog:
    def __init__(self, base_path: Optional[Path] = None):
        if base_path is None:
            # Set base_path to the parent directory of the directory where catalog.py is located
            base_path = Path(__file__).resolve().parent.parent
        self.base_path = base_path
        self.data_path = base_path / "data"
        self.tasks_path = self.data_path / "tasks/tasks.jsonl"
        self.icl_prompts_path = self.data_path / "icl_prompts/icl_prompts.jsonl"
        self.articulation_prompts_path = (
            self.data_path / "articulation_prompts/articulation_prompts.jsonl"
        )
        self.figures_path = base_path / "figures"
        self.interaction_path = base_path / "owain_app"
        self.test_path = base_path / "tests"

    def _save_jsonl(self, path: Path, items: list[BaseModel], schema: type[BaseModel]):
        logger.info(f"Saving {schema.__name__} instances to {path}")
        logger.info(f"Number of instances: {len(items)}")
        if not path.parent.exists():
            logger.info(f"Creating directory {path.parent}")
            path.parent.mkdir(parents=True)
        with open(path, "w") as f:
            for item in items:
                json.dump(item.dict(), f)
                f.write("\n")

    def _load_jsonl(self, path: Path, schema: type[BaseModel]):
        logger.info(f"Loading {schema.__name__} instances from {path}")
        with open(path, "r") as f:
            items = [schema(**json.loads(line)) for line in f]
        return items

    def load_tasks(self) -> list[Task]:
        return self._load_jsonl(self.tasks_path, Task)  # type: ignore

    def save_tasks(self, tasks: list[Task]):
        self._save_jsonl(self.tasks_path, tasks, Task)  # type: ignore

    def save_icl_prompts(self, prompts: List[ICLPrompt]):
        self._save_jsonl(self.icl_prompts_path, prompts, ICLPrompt)  # type: ignore

    def load_icl_prompts(self) -> List[ICLPrompt]:
        return self._load_jsonl(self.icl_prompts_path, ICLPrompt)  # type: ignore

    def save_articulation_prompts(self, prompts: List[ICLPrompt]):
        self._save_jsonl(self.articulation_prompts_path, prompts, ICLPrompt)  # type: ignore

    def load_articulation_prompts(self) -> List[ICLPrompt]:
        return self._load_jsonl(self.articulation_prompts_path, ICLPrompt)  # type: ignore
