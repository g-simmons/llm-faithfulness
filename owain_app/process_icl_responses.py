from owain_app.catalog import Catalog
from owain_app.schemas import (
    ICLPromptResponse,
    ProcessedICLPromptResponse
)

MODEL_NAME = "gpt-4"


def convert_from_request(response: ICLPromptResponse) -> ProcessedICLPromptResponse:
    return ProcessedICLPromptResponse(
        model=MODEL_NAME,
        prompt=response.input["messages"][0]["content"],
        prediction=response.output["choices"][0]["message"]["content"],
        **response.metadata.model_dump(),
    )

def main():
    catalog = Catalog()
    responses = catalog.load_icl_responses()
    processed_responses = [convert_from_request(response) for response in responses]
    catalog.save_processed_icl_responses(processed_responses)


if __name__ == "__main__":
    main()
