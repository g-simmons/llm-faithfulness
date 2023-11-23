from pydantic import BaseModel, conint
from typing import List, Tuple, Optional

class Rule(BaseModel):
    index: conint(ge=0)  # Rule index (e.g., 0 for the first rule)
    value: bool          # Rule value (True or False)

class DatasetPartitionerInput(BaseModel):
    n: conint(ge=1)           # Number of binary digits, must be >= 1
    rules: List[Rule]         # List of rules

class DatasetPartitionerOutput(BaseModel):
    rule_names: List[str]     # Names of the rules used
    train_dataset_size: int   # Number of examples in the training dataset
    test_dataset_size: int    # Number of examples in the test dataset

class OpenAIInteractionInput(BaseModel):
    prompt: str               # Prompt to be sent to the OpenAI API
    model: str                # OpenAI model to be used

class OpenAIInteractionOutput(BaseModel):
    response: str             # Response from the OpenAI API

class KFoldValidationInput(BaseModel):
    n_splits: conint(gt=1)    # Number of splits for k-fold, greater than 1
    dataset_size: int         # Size of the dataset to be split

class KFoldValidationOutput(BaseModel):
    fold_results: List[Tuple[int, float]]  # List of tuples (fold number, accuracy)
    average_accuracy: Optional[float]      # Average accuracy across all folds
