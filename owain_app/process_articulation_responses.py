from owain_app.catalog import Catalog
from owain_app.schemas import (
    ArticulationPromptResponse,
    ProcessedArticulationPromptResponse
)

MODEL_NAME = "gpt-4"


def convert_from_request(response: ArticulationPromptResponse) -> ProcessedArticulationPromptResponse:
    return ProcessedArticulationPromptResponse(
        model=MODEL_NAME,
        prompt=response.input["messages"][0]["content"],
        prediction_str=response.output["choices"][0]["message"]["content"],
        **response.metadata.model_dump(),
    )

def main():
    catalog = Catalog()
    responses = catalog.load_articulation_responses()
    processed_responses = [convert_from_request(response) for response in responses]
    catalog.save_processed_articulation_responses(processed_responses)


if __name__ == "__main__":
    main()
