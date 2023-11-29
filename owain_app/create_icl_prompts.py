import click
from owain_app.catalog import Catalog
from loguru import logger

from owain_app.schemas import Task, ICLPrompt
from typing import List, Tuple


EXAMPLE_TEMPlATE = "input: {input}; label: {label}"
INSTRUCTIONS = "Classify the unlabeled example from the labeled examples. Respond with a single binary digit indicating the label."


def make_icl_prompt(
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


def task_to_icl_prompts(task: Task) -> List[ICLPrompt]:
    prompts = [
        make_icl_prompt(
            train_examples=[
                (s, str(int(l))) for s, l in zip(task.train_examples, task.train_labels)
            ],
            test_example=test_example,
        )
        for test_example in task.test_examples
    ]
    return prompts


@click.command()
def main():
    # Initialize Catalog
    catalog = Catalog()  # Assuming Catalog is set up with the correct base_path
    tasks = catalog.load_tasks()
    prompts = []
    for task in tasks:
        prompts.extend(task_to_icl_prompts(task))

    catalog.save_prompts(prompts)


if __name__ == "__main__":
    main()
