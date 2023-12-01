from pydantic import BaseModel, conint
from typing import Optional, Callable
from enum import Enum


class NotationType(str, Enum):
    string = "string"
    set = "set"


class Split(str, Enum):
    val = "val"
    test = "test"


class Rule(BaseModel):
    rule: Callable
    rule_name: str

    def json(self, **kwargs):
        include = getattr(self.Config, "include", set())
        if len(include) == 0:
            include = None
        exclude = getattr(self.Config, "exclude", set())
        if len(exclude) == 0:
            exclude = None
        return super().model_dump_json(include=include, exclude=exclude, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.rule(*args, **kwargs)

    class Config:
        exclude = {"rule"}
        arbitrary_types_allowed = True


class Task(BaseModel):
    notation_type: NotationType
    string_length: conint(ge=1)  # Length of binary strings # type: ignore
    train_rule_names: list[str]
    train_examples: list[str]
    train_labels: list[int]
    test_examples: list[str]
    val_examples: Optional[list[str]] = None
    val_labels: Optional[list[int]] = None

    @property
    def name(self):
        return "_".join(self.train_rule_names)


class ICLPrompt(BaseModel):
    string_length: conint(ge=1)  # type: ignore
    notation_type: str
    train_rule_names: list[str]
    train_examples: list[str]
    train_labels: list[int]
    test_example: str
    test_label: Optional[int] = None
    prompt: str
    split: Split


class ICLPromptMetadata(BaseModel):
    string_length: conint(ge=1)  # type: ignore
    notation_type: str
    train_rule_names: list[str]
    train_examples: list[str]
    train_labels: list[int]
    test_example: str
    test_label: Optional[int] = None
    split: Split


class ArticulationPrompt(BaseModel):
    string_length: conint(ge=1)  # type: ignore
    notation_type: str
    train_rule_names: list[str]
    train_examples: list[str]
    train_labels: list[int]
    answer_options: list[str]
    answer_option_rule_names: list[tuple[str, ...]]
    correct_answer_letters: list[str]
    incorrect_answer_letters: list[str]
    prompt: str
    # split: Split


class ArticulationPromptMetadata(BaseModel):
    string_length: conint(ge=1)  # type: ignore
    notation_type: str
    # train_rules: list[Rule]
    train_rule_names: list[str]
    train_examples: list[str]
    train_labels: list[int]
    answer_options: list[str]
    answer_option_rule_names: list[tuple[str, ...]]
    correct_answer_letters: list[str]
    # split: Split


class PromptMessage(BaseModel):
    role: str
    content: str


class ICLPromptRequest(BaseModel):
    model: str
    max_tokens: int
    messages: list[PromptMessage]
    metadata: ICLPromptMetadata


class ArticulationPromptRequest(BaseModel):
    model: str
    max_tokens: int
    messages: list[PromptMessage]
    metadata: ArticulationPromptMetadata
    n: int = 1



class ICLPromptResponse(BaseModel):
    input: dict
    output: dict
    metadata: ICLPromptMetadata


class ArticulationPromptResponse(BaseModel):
    input: dict
    output: dict
    metadata: ArticulationPromptMetadata

class ProcessedICLPromptResponse(BaseModel):
    string_length: conint(ge=1)  # type: ignore
    notation_type: str
    # train_rules: list[Rule]
    train_rule_names: list[str]
    train_examples: list[str]
    train_labels: list[int]
    test_example: str
    test_label: Optional[int] = None
    prompt: str
    prediction: str
    model: str
    split: Split


class ProcessedArticulationPromptResponse(BaseModel):
    string_length: conint(ge=1)  # type: ignore
    notation_type: str
    # train_rules: list[Rule]
    train_rule_names: list[str]
    train_examples: list[str]
    train_labels: list[int]
    # split: Split
    answer_options: list[str]
    answer_option_rule_names: list[tuple[str, ...]]
    correct_answer_letters: list[str]
    prompt: str
    prediction_str: str
    model: str
    # split: Split
