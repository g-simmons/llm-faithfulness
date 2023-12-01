from owain_app.catalog import Catalog

from owain_app.schemas import Task, ICLPrompt, Split
from typing import List, Tuple


EXAMPLE_TEMPlATE = "input: {input}; label: {label}"
INSTRUCTIONS = "Classify the unlabeled example from the labeled examples. Respond with a single binary digit indicating the label."


def format_train_examples(
    train_examples: List[str], train_labels: List[int], example_template: str
):
    example_content = [
        example_template.format(input=x, label=y)
        for x, y in zip(train_examples, train_labels)
    ]
    example_content = "\n".join(example_content)
    return example_content


def make_icl_prompt(
    train_examples: List[str],
    train_labels: List[int],
    test_example: str,
    example_template: str = EXAMPLE_TEMPlATE,
    instructions: str = INSTRUCTIONS,
):
    example_content = format_train_examples(
        train_examples, train_labels, example_template
    )
    test_content = example_template.format(input=test_example, label="")

    return (
        instructions
        + "\n\nLabeled Examples:\n```\n"
        + example_content
        + "\n```\n\nUnlabeled Example:\n```\n"
        + test_content
    )


def task_to_icl_prompts(task: Task) -> List[ICLPrompt]:
    all_prompts = []
    assert task.val_examples is not None
    test_labels = [None]*len(task.test_examples) #type: list[int|None]
    assert test_labels is not None
    for examples, labels, split_name in zip(
        [task.val_examples, task.test_examples],
        [task.val_labels, test_labels],
        [Split.val, Split.test],
    ):
        prompts = [
            make_icl_prompt(
                train_examples=task.train_examples,
                train_labels=task.train_labels,
                test_example=test_example,
            )
            for test_example in examples
        ]
        prompts = [
            ICLPrompt(
                string_length=task.string_length,
                notation_type=task.notation_type,
                train_rule_names=task.train_rule_names,
                train_examples=task.train_examples,
                train_labels=task.train_labels,
                test_example=test_example,
                test_label=test_label,
                prompt=prompt,
                split=split_name,
            )
            for test_example, test_label, prompt in zip(examples, labels, prompts) #type: ignore
        ]
        all_prompts.extend(prompts)

    return all_prompts


def main():
    # Initialize Catalog
    catalog = Catalog()  # Assuming Catalog is set up with the correct base_path
    tasks = catalog.load_tasks()
    prompts = []
    for task in tasks:
        prompts.extend(task_to_icl_prompts(task))

    catalog.save_icl_prompts(prompts)


if __name__ == "__main__":
    main()
