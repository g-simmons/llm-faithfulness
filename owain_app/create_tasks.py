import itertools
import random
from owain_app.schemas import Rule, Task
from owain_app.catalog import Catalog
from loguru import logger
import click


def generate_binary_strings(string_length):
    return ["".join(s) for s in itertools.product("01", repeat=string_length)]


def apply_rules(s, rules):
    if all((r(s) for r in rules)):
        return True
    elif all((not r(s) for r in rules)):
        return False
    else:
        return None


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
    train_examples = [
        s
        for s in binary_strings
        if apply_rules(s, rule_combination) is True
        or apply_rules(s, rule_combination) is False
    ]
    test_examples = [
        s for s in binary_strings if apply_rules(s, rule_combination) is None
    ]

    return Task(
        train_rules=rule_combination,
        train_examples=train_examples,
        train_labels=[apply_rules(s, rule_combination) for s in binary_strings],
        test_examples=test_examples,
    )


def train_val_split(task: Task, val_pct: float) -> Task:
    train_val_split_index = int(len(task.train_examples) * (1 - val_pct))
    train_examples = task.train_examples[:train_val_split_index]
    train_labels = task.train_labels[:train_val_split_index]
    val_examples = task.train_examples[train_val_split_index:]
    val_labels = task.train_labels[train_val_split_index:]

    return Task(
        train_rules=task.train_rules,
        train_examples=train_examples,
        train_labels=train_labels,
        val_examples=val_examples,
        val_labels=val_labels,
        test_examples=task.test_examples,
    )


def get_all_rules(string_length):
    rules = [lambda s, i=i: s[i] == "1" for i in range(string_length)]
    rule_names = [f"rule{i}" for i in range(string_length)]
    rules = [
        Rule(rule=rule, rule_name=rule_name)
        for rule, rule_name in zip(rules, rule_names)
    ]
    return rules


def convert_to_set_notation(string_notation_task: Task) -> Task:
    return Task(
        train_rules=string_notation_task.train_rules,
        train_examples=[
            convert_to_set_notation(s) for s in string_notation_task.train_examples
        ],
        train_labels=string_notation_task.train_labels,
        val_examples=[
            convert_to_set_notation(s) for s in string_notation_task.val_examples
        ],
        val_labels=string_notation_task.val_labels,
        test_examples=[
            convert_to_set_notation(s) for s in string_notation_task.test_examples
        ],
    )


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
