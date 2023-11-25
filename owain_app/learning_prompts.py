import openai
import numpy as np
import click
from pathlib import Path
import itertools
import json
import os
from sklearn.model_selection import KFold
from dotenv import load_dotenv
from owain_app.catalog import Catalog
from loguru import logger

# from owain_app.schemas import BinaryString, Label
from typing import List, Tuple

EXAMPLE_TEMPlATE = "input: {input}; label: {label}"
INSTRUCTIONS = "Classify the unlabeled example from the labeled examples. Respond with a single binary digit indicating the label."


def make_prompt(
    train_examples: List[Tuple],
    test_example: str,
    example_template: str = EXAMPLE_TEMPlATE,
    instructions: str = INSTRUCTIONS,
):
    example_content = [
        example_template.format(input=x, label=y) for x, y in train_examples
    ]
    example_content = "\n".join(example_content)
    test_content = example_template.format(input=test_example, label="")

    return (
        instructions
        + "\n\nLabeled Examples:\n```\n"
        + example_content
        + "\n```\n\nUnlabeled Example:\n```\n"
        + test_content
    )


def query_openai_api(prompt, model="text-davinci-003"):
    load_dotenv()
    api_key = os.getenv("API_KEY")
    openai.api_key = api_key
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=150)
    return response.choices[0].text.strip()


@click.command()
@click.option("--n", type=int, default=4, help="Length of binary strings")
@click.option("--r", type=int, default=2, help="Number of rules to apply")
def main(n, r):
    # Initialize Catalog
    catalog = Catalog()  # Assuming Catalog is set up with the correct base_path
    possible_rules = [lambda s, i=i: s[i] == "1" for i in range(n)]

    for combination in itertools.combinations(possible_rules, r):
        logger.info(
            f"Starting prompt generation for combination {combination}"
        )  # Added logging statement
        rule_names = [f"rule{possible_rules.index(rule)}" for rule in combination]

        # Load dataset using Catalog
        dataset = catalog.load_task(4, rule_names, notation_type="string_notation")
        filename = f"data/prompts/n={n}/{'_and_'.join(rule_names)}/all.jsonl"
        filename = Path(filename)
        # Save prompt to file
        if not filename.parent.exists():
            filename.parent.mkdir(parents=True)

        # if filename exists, overwrite it
        if filename.exists():
            filename.unlink()

        for i, (test_example, test_label) in enumerate(dataset["test"]):
            # Make prompt
            prompt = make_prompt(dataset["train"], test_example)
            with open(filename, "a") as f:
                prompt_with_metadata = json.dumps(
                    {
                        "prompt": prompt,
                        "train_examples": dataset["train"],
                        "test_example": test_example,
                        "rule_names": rule_names,
                        "split": "test",
                        "label": None
                    }
                )
                f.write(prompt_with_metadata + "\n")

        for i, (test_example, test_label) in enumerate(dataset["val"]):
            # Make prompt
            prompt = make_prompt(dataset["train"], test_example)
            with open(filename, "a") as f:
                prompt_with_metadata = json.dumps(
                    {
                        "prompt": prompt,
                        "train_examples": dataset["train"],
                        "test_example": test_example,
                        "rule_names": rule_names,
                        "split": "val",
                        "label": test_label
                    }
                )
                f.write(prompt_with_metadata + "\n")


if __name__ == "__main__":
    main()
