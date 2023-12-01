from owain_app.catalog import Catalog
from owain_app.schemas import (
    ICLPrompt,
    ICLPromptRequest,
    PromptMessage,
    ICLPromptMetadata,
)

MODEL_NAME = "gpt-4"


def convert_to_request(prompt: ICLPrompt) -> ICLPromptRequest:
    return ICLPromptRequest(
        model=MODEL_NAME,
        max_tokens=1,
        messages=[
            PromptMessage(role="user", content=prompt.prompt),
        ],
        metadata=ICLPromptMetadata(**prompt.model_dump()),
    )


def main():
    catalog = Catalog()
    prompts = catalog.load_icl_prompts()
    requests = [convert_to_request(prompt) for prompt in prompts]
    catalog.save_icl_requests(requests)


if __name__ == "__main__":
    main()
