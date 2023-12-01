import click
import string
import random
import itertools
from itertools import combinations, permutations, product
from owain_app.catalog import Catalog
from loguru import logger

from owain_app.schemas import Task, ArticulationPrompt
from owain_app.create_tasks import get_all_rules
from typing import List, Tuple


ARTICULATION_EXAMPLE_TEMPlATE = "input: {input}; label: {label}"
ARTICULATON_INSTRUCTIONS = """Select the rule that you would use to classify unlabeled examples for the task demonstrated by the labeled examples. 
Each example is a string consisting of binary digits 0 and 1. 

Each rule is a logical expression consisting of binary variables x0, x1, x2, ..., xN, where N is the length of the string.

Select the rule that you would use to classify unlabeled examples for the task demonstrated by the labeled examples.

Respond with a single letter."""

def format_train_examples(
    train_examples: List[str], train_labels: List[int], example_template: str
):
    example_content = [
        example_template.format(input=x, label=y)
        for x, y in zip(train_examples, train_labels)
    ]
    example_content = "\n".join(example_content)
    return example_content


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


def format_rule(rule: str):
    rule_number = rule.lstrip("rule")
    rule_number = int(rule_number)
    rule_string = f"x{rule_number} == 1"
    return rule_string


from collections import namedtuple

AnswerOptionSet = namedtuple(
    "AnswerOptionSet", ["correct_options", "incorrect_options"]
)


def get_answer_option_sets(
    task: Task,
    min_rules_per_answer: int,
    num_correct_answers: int = 1,
    num_incorrect_answers: int = 3,
) -> List[AnswerOptionSet]:
    # correct answers are all the unique orderings of the train rules
    correct_answer_options = list(itertools.permutations(task.train_rule_names))
    # incorrect answers are all the unique orderings of rule combinations
    # with length min_rules_per_answer to len(task.train_rule_names)
    # that do not match the train rule combinations
    all_rules = get_all_rules(string_length=task.string_length)
    all_rules = [r.rule_name for r in all_rules]
    all_rule_combinations = list(
        itertools.chain.from_iterable(
            combinations(all_rules, r)
            for r in range(min_rules_per_answer, len(task.train_rule_names) + 1)
        )
    )

    incorrect_answer_options = []
    for rule_combination in all_rule_combinations:
        if rule_combination not in correct_answer_options:
            incorrect_answer_options.append(rule_combination)

    answer_option_sets = [
        AnswerOptionSet(
            correct_options=correct_options,
            incorrect_options=incorrect_options,
        )
        for correct_options, incorrect_options in product(
            combinations(correct_answer_options, num_correct_answers),
            combinations(incorrect_answer_options, num_incorrect_answers),
        )
    ]

    return answer_option_sets


def format_prompt_text(instructions: str, example_content: str, answer_content: str):
    prompt_text = """
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
    return prompt_text


def get_answer_letters(correct_options, incorrect_options):
    num_answers = len(correct_options) + len(incorrect_options)
    answer_letters = list(string.ascii_uppercase)[:num_answers]
    return answer_letters


def get_correct_incorrect_indices(shuffled_options, correct_options, incorrect_options):
    correct_answer_indices = [
        i for i, option in enumerate(shuffled_options) if option in correct_options
    ]
    incorrect_answer_indices = [
        i for i, option in enumerate(shuffled_options) if option in incorrect_options
    ]
    return correct_answer_indices, incorrect_answer_indices


def make_articulation_prompts(
    task: Task,
    min_rules_per_answer: int,
    num_correct_answers: int,
    num_incorrect_answers: int,
    example_template: str = ARTICULATION_EXAMPLE_TEMPlATE,
    instructions: str = ARTICULATON_INSTRUCTIONS,
):
    prompts = []
    example_content = format_train_examples(
        task.train_examples, task.train_labels, example_template
    )
    answer_option_sets = get_answer_option_sets(
        task, min_rules_per_answer, num_correct_answers, num_incorrect_answers
    )
    for correct_options, incorrect_options in answer_option_sets:
        answer_letters = get_answer_letters(correct_options, incorrect_options)
        shuffled_options = list(correct_options + incorrect_options)
        random.shuffle(shuffled_options)
        (
            correct_answer_indices,
            incorrect_answer_indices,
        ) = get_correct_incorrect_indices(
            shuffled_options, correct_options, incorrect_options
        )
        answer_options = [
            f"{letter}: {' and '.join([format_rule(r) for r in rules])}"
            for letter, rules in zip(answer_letters, shuffled_options)
        ]
        answer_content = "\n".join(answer_options)
        correct_answer_letters = [answer_letters[i] for i in correct_answer_indices]
        incorrect_answer_letters = [answer_letters[i] for i in incorrect_answer_indices]
        prompt_text = format_prompt_text(instructions, example_content, answer_content)
        prompt = ArticulationPrompt(
            string_length=task.string_length,
            notation_type=task.notation_type,
            train_rule_names=task.train_rule_names,
            train_examples=task.train_examples,
            train_labels=task.train_labels,
            answer_options=answer_options,
            answer_option_rule_names=shuffled_options,
            correct_answer_letters=correct_answer_letters,
            incorrect_answer_letters=incorrect_answer_letters,
            prompt=prompt_text,
        )
        prompts.append(prompt)
    return prompts


@click.command()
def main():
    catalog = Catalog()
    tasks = catalog.load_tasks()
    prompts = []
    for task in tasks:
        prompts.extend(
            make_articulation_prompts(
                task,
                min_rules_per_answer=1,
                num_correct_answers=1,
                num_incorrect_answers=3,
            )
        )

    catalog.save_articulation_prompts(prompts)


if __name__ == "__main__":
    main()
