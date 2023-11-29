import click
import string
import itertools
from owain_app.catalog import Catalog
from loguru import logger

from owain_app.schemas import Task, Rule, ArticulationPrompt
from typing import List, Tuple


ARTICULATION_EXAMPLE_TEMPlATE = "input: {input}; label: {label}"
ARTICULATON_INSTRUCTIONS = "Select the rule that you would use to classify unlabeled examples for the task demonstrated by the labeled examples. Respond with a single letter."


def make_articulation_prompt(
    train_examples: List[Tuple],
    train_rules: List[Rule],
    rules_per_answer: int,
    num_correct_answers: int,
    example_template: str = ARTICULATION_EXAMPLE_TEMPlATE,
    instructions: str = ARTICULATON_INSTRUCTIONS,
):
    example_content = [
        example_template.format(input=x, label=y) for x, y in train_examples
    ]
    example_content = "\n".join(example_content)
    answer_options = [
        rules
        for rules in itertools.combinations(train_rules, rules_per_answer)
        if sum(r in rules for r in train_rules) == num_correct_answers
    ]
    answer_letters = list(string.ascii_uppercase)[: len(answer_options)]
    answer_content = "\n".join(
        [
            f"{letter}: {' '.join([r.rule_name for r in rules])}"
            for letter, rules in zip(answer_letters, answer_options)
        ]
    )

    return """
    {}
    
    Labeled Examples:
    ```
    {}
    ```

    Answer Options:
    ```
    {}
    ```""".format(
        instructions, example_content, answer_content
    )


def task_to_articulation_prompts(task: Task) -> List[ArticulationPrompt]:
    prompts = [
        make_articulation_prompt(
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
    catalog = Catalog()
    tasks = catalog.load_tasks()
    prompts = []
    for task in tasks:
        prompts.extend(task_to_articulation_prompts(task))

    catalog.save_prompts(prompts)


if __name__ == "__main__":
    main()
