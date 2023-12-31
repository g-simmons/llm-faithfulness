import itertools
import random
from typing import Union
from owain_app.schemas import Rule, Task, NotationType
from owain_app.catalog import Catalog
from loguru import logger
from sklearn.model_selection import train_test_split
import click


def generate_binary_strings(string_length):
    return ["".join(s) for s in itertools.product("01", repeat=string_length)]


def apply_rules(s, rules) -> Union[int, None]:
    if all([r(s) for r in rules]):
        return 1
    elif all([(not r(s)) for r in rules]):
        return 0
    else:
        return None

def get_rule_by_rule_name(rule_name: str) -> Rule:
    rules = get_all_rules(string_length=20)
    rule = [r for r in rules if r.rule_name == rule_name][0]
    return rule

def convert_to_set_notation(s):
    if len(s) > 20:
        raise ValueError("String length must be <= 20")
    return {
        f'{"one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()[i]}'
        for i, char in enumerate(s)
        if char == "1"
    }


def get_task_for_rule_combination(
    rule_combination: tuple[Rule], binary_strings: list[str]
) -> Task:
    assert set([len(x) for x in binary_strings]) == {len(binary_strings[0])}
    train_examples_labels = [
        (s, apply_rules(s, rule_combination))
        for s in binary_strings
        if (
            (apply_rules(s, rule_combination) is 1)  # ignore the SyntaxWarning here
            or (apply_rules(s, rule_combination) is 0)
        )  # ignore the SyntaxWarning here
    ]

    train_examples, train_labels = zip(*train_examples_labels)
    test_examples = [
        s for s in binary_strings if apply_rules(s, rule_combination) is None
    ]
    train_examples = list(str(x) for x in train_examples)
    train_labels = list(int(x) for x in train_labels)  # type: ignore

    return Task(
        notation_type=NotationType.string,
        train_rule_names=[r.rule_name for r in rule_combination],
        train_examples=list(train_examples),
        train_labels=list(train_labels),
        test_examples=test_examples,
        string_length=len(binary_strings[0]),
    )


def train_val_split(task: Task, val_pct: float) -> Task:
    train_examples, val_examples, train_labels, val_labels = train_test_split(
        task.train_examples,
        task.train_labels,
        test_size=val_pct,
        random_state=42,
    )

    return Task(
        notation_type=task.notation_type,
        train_rule_names=task.train_rule_names,
        train_examples=train_examples,
        train_labels=train_labels,
        val_examples=val_examples,
        val_labels=val_labels,
        test_examples=task.test_examples,
        string_length=task.string_length,
    )


def get_all_rules(string_length):
    rules = [lambda s, i=i: s[i] == "1" for i in range(string_length)]
    rule_names = [f"rule{i}" for i in range(string_length)]
    rules = [
        Rule(rule=rule, rule_name=rule_name)
        for rule, rule_name in zip(rules, rule_names)
    ]
    return rules


# def convert_to_set_notation(string_notation_task: Task) -> Task:
#     return Task(
#         notation_type="set",
#         train_rules=string_notation_task.train_rules,
#         train_examples=[
#             convert_to_set_notation(s) for s in string_notation_task.train_examples
#         ],
#         train_labels=string_notation_task.train_labels,
#         val_examples=[
#             convert_to_set_notation(s) for s in string_notation_task.val_examples
#         ],
#         val_labels=string_notation_task.val_labels,
#         test_examples=[
#             convert_to_set_notation(s) for s in string_notation_task.test_examples
#         ],
#     )


@click.command()
@click.option("--n", type=int, default=4, help="Length of binary strings")
@click.option("--r", type=int, default=2, help="Number of rules to apply")
@click.option(
    "--val-pct", type=float, default=0.2, help="percent of data to use for validation"
)
def main(n, r, val_pct):
    logger.info(f"Starting dataset generation with n={n} and r={r}")
    binary_strings = generate_binary_strings(string_length=n)
    rules = get_all_rules(string_length=n)
    catalog = Catalog()
    rule_combinations = list(itertools.combinations(rules, r))
    tasks = [
        train_val_split(
            get_task_for_rule_combination(rule_combination, binary_strings),
            val_pct=val_pct,
        )
        for rule_combination in rule_combinations
    ]
    catalog.save_tasks(tasks)


if __name__ == "__main__":
    main()
