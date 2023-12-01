from owain_app.catalog import Catalog
from owain_app.create_tasks import get_rule_by_rule_name, apply_rules

catalog = Catalog()

icl_prompts = catalog.load_icl_prompts()


def test_icl_prompts():
    for prompt in icl_prompts:
        rule_names = prompt.train_rule_names
        rules = [get_rule_by_rule_name(rule_name) for rule_name in rule_names]
        for train_example, train_label in zip(
            prompt.train_examples, prompt.train_labels
        ):
            assert apply_rules(train_example, rules) == train_label

        if prompt.split == "val":
            assert apply_rules(prompt.test_example, rules) in [0, 1]

        elif prompt.split == "test":
            assert apply_rules(prompt.test_example, rules) is None