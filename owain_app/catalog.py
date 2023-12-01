import json
from typing import List, Union, Optional
from owain_app.schemas import (
    Task,
    ICLPrompt,
    ICLPromptRequest,
    ArticulationPrompt,
    ArticulationPromptRequest,
    ICLPromptResponse,
    ProcessedArticulationPromptResponse,
    ProcessedICLPromptResponse,
    ArticulationPromptResponse
)

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
        self.icl_requests_path = self.data_path / "icl_requests/icl_requests.jsonl"
        self.icl_responses_path = self.data_path / "icl_responses/icl_responses.jsonl"
        self.articulation_prompts_path = (
            self.data_path / "articulation_prompts/articulation_prompts.jsonl"
        )
        self.articulation_requests_path = (
            self.data_path / "articulation_requests/articulation_requests.jsonl"
        )
        self.articulation_responses_path = (
            self.data_path / "articulation_responses/articulation_responses.jsonl"
        )
        self.processed_icl_responses_path = (
            self.data_path / "processed_icl_responses/processed_icl_responses.jsonl"
        )
        self.processed_articulation_responses_path = (
            self.data_path / "processed_articulation_responses/processed_articulation_responses.jsonl"
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

    def _load_jsonl(self, path: Path, schema: type[BaseModel], line_fn = lambda x: x):
        logger.info(f"Loading {schema.__name__} instances from {path}")
        with open(path, "r") as f:
            items = [schema(**line_fn(json.loads(line))) for line in f]
        return items

    def load_tasks(self) -> list[Task]:
        return self._load_jsonl(self.tasks_path, Task)  # type: ignore

    def save_tasks(self, tasks: list[Task]):
        self._save_jsonl(self.tasks_path, tasks, Task)  # type: ignore

    def save_icl_prompts(self, prompts: List[ICLPrompt]):
        self._save_jsonl(self.icl_prompts_path, prompts, ICLPrompt)  # type: ignore

    def load_icl_prompts(self) -> List[ICLPrompt]:
        return self._load_jsonl(self.icl_prompts_path, ICLPrompt)  # type: ignore

    def save_icl_requests(self, requests: List[ICLPromptRequest]):
        self._save_jsonl(self.icl_requests_path, requests, ICLPromptRequest)  # type: ignore

    def save_processed_icl_responses(self, responses: List[ProcessedICLPromptResponse]):
        self._save_jsonl(self.processed_icl_responses_path, responses, ProcessedICLPromptResponse)  # type: ignore
    
    def load_processed_icl_responses(self) -> List[ProcessedICLPromptResponse]:
        return self._load_jsonl(self.processed_icl_responses_path, ProcessedICLPromptResponse) # type: ignore

    def save_articulation_prompts(self, prompts: List[ArticulationPrompt]):
        self._save_jsonl(self.articulation_prompts_path, prompts, ArticulationPrompt)  # type: ignore

    def load_articulation_prompts(self) -> List[ArticulationPrompt]:
        return self._load_jsonl(self.articulation_prompts_path, ArticulationPrompt)  # type: ignore

    def save_articulation_requests(self, requests: List[ArticulationPromptRequest]):
        self._save_jsonl(self.articulation_requests_path, requests, ArticulationPromptRequest)  # type: ignore
    
    def save_processed_articulation_responses(self, responses: List[ProcessedArticulationPromptResponse]): 
        self._save_jsonl(self.processed_articulation_responses_path, responses, ProcessedArticulationPromptResponse) # type: ignore

    def load_processed_articulation_responses(self) -> List[ProcessedArticulationPromptResponse]:
        return self._load_jsonl(self.processed_articulation_responses_path, ProcessedArticulationPromptResponse) # type: ignore

    def load_articulation_requests(self) -> List[ArticulationPromptRequest]:
        return self._load_jsonl(self.articulation_requests_path, ArticulationPromptRequest)  # type: ignore
    
    def load_icl_responses(self) -> List[ICLPromptResponse]:
        return self._load_jsonl(self.icl_responses_path, ICLPromptResponse, lambda x: {"input": x[0],"output":x[1],"metadata":x[2]})  # type: ignore

    def load_articulation_responses(self) -> List[ArticulationPromptResponse]:
        return self._load_jsonl(self.articulation_responses_path, ArticulationPromptResponse, lambda x: {"input": x[0],"output":x[1],"metadata":x[2]}) # type: ignore
