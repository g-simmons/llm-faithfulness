from pydantic import BaseModel, constr, conint
from enum import Enum


class NotationType(str, Enum):
    string = "string"
    set = "set"


class Rule(BaseModel):
    rule: callable
    rule_name: str


class StringNotationTask(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[bool]
    val_examples: list[str]
    val_labels: list[bool]
    test_examples: list[str]

    @property
    def name(self):
        return "_".join([rule.rule_name for rule in self.train_rules])


class BinaryString(BaseModel):
    value: constr(regex="^[01]+$")  # one or more 0s or 1s


class Label(BaseModel):
    value: constr(regex="^[01]$")  # a single 0 or 1


class ICLPrompt(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[bool]
    test_example: str
    prompt: str


class ICLPromptMetadata(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[bool]
    test_example: str


class ArticulationPrompt(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[bool]
    answer_options: list[tuple[Rule]]
    correct_answer_letters: list[str]
    prompt: str


class ArticulationPromptMetadata(BaseModel):
    string_length: conint(ge=1)  # Length of binary strings
    notation_type: str
    train_rules: list[Rule]
    train_examples: list[str]
    train_labels: list[bool]
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
    train_labels: list[bool]
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
    train_labels: list[bool]
    answer_options: list[tuple[Rule]]
    correct_answer_letters: list[str]
    prompt: str
    response: OpenAIResponse
    model_prediction_str: str
    model_prediction_rules: tuple[Rule]
    model_confidence: float

