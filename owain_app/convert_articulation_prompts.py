from owain_app.catalog import Catalog
from owain_app.schemas import (
    ArticulationPrompt,
    ArticulationPromptRequest,
    PromptMessage,
    ArticulationPromptMetadata,
)
from random import sample

MODEL_NAME = "gpt-4"


def convert_to_request(prompt: ArticulationPrompt) -> ArticulationPromptRequest:
    return ArticulationPromptRequest(
        model=MODEL_NAME,
        max_tokens=1,
        n=5,
        messages=[
            PromptMessage(role="user", content=prompt.prompt),
        ],
        metadata=ArticulationPromptMetadata(**prompt.model_dump()),
    )


def main():
    catalog = Catalog()
    prompts = catalog.load_articulation_prompts()
    requests = [convert_to_request(prompt) for prompt in prompts]
    catalog.save_articulation_requests(requests)


if __name__ == "__main__":
    main()
