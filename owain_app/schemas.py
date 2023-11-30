from pydantic import BaseModel, constr, conint, ConfigDict
from enum import Enum


class NotationType(str, Enum):
    string = "string"
    set = "set"


class Rule(BaseModel):
    rule: callable
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
    string_length: conint(ge=1)  # Length of binary strings
    # train_rules: list[Rule]
    train_rule_names: list[str]
    train_examples: list[str]
    train_labels: list[int]
    test_examples: list[str]
    val_examples: list[str] = None
    val_labels: list[int] = None

    @property
    def name(self):
        return "_".join(self.train_rule_names)


class ICLPrompt(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[int]
    test_example: str
    prompt: str


class ICLPromptMetadata(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[int]
    test_example: str


class ArticulationPrompt(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[int]
    answer_options: list[tuple[Rule]]
    correct_answer_letters: list[str]
    prompt: str


class ArticulationPromptMetadata(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[int]
    answer_options: list[tuple[Rule]]
    correct_answer_letters: list[str]


class PromptMessage(BaseModel):
    role: str
    message: str


class ICLPromptRequest(BaseModel):
    model: str
    messages: list[PromptMessage]
    metadata: ICLPromptMetadata


class ArticulationPromptRequest(BaseModel):
    model: str
    messages: list[PromptMessage]
    metadata: ArticulationPromptMetadata


class OpenAIResponse(BaseModel):
    choices: list[dict]


class ICLPromptResponse(BaseModel):
    model: str
    messages: list[PromptMessage]
    metadata: ICLPromptMetadata
    response: OpenAIResponse


class ArticulationPromptResponse(BaseModel):
    model: str
    messages: list[PromptMessage]
    metadata: ArticulationPromptMetadata
    response: OpenAIResponse

class ProcessedICLPromptResponse(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[int]
    test_example: str
    prompt: str
    response: OpenAIResponse
    model_prediction: str
    model_confidence: float

class ProcessedArticulationPromptResponse(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[int]
    answer_options: list[tuple[Rule]]
    correct_answer_letters: list[str]
    prompt: str
    response: OpenAIResponse
    model_prediction_str: str
    model_prediction_rules: tuple[Rule]
    model_confidence: float

