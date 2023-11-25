import itertools
import random
from owain_app.catalog import Catalog
from loguru import logger
import click


def generate_binary_strings(n):
    return ["".join(s) for s in itertools.product("01", repeat=n)]


def apply_rules(s, rules):
    return all(r(s) for r in rules)


def anti_apply_rules(s, rules):
    return not all((not r(s)) for r in rules)


def convert_to_set_notation(s):
    return {
        f'{"one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()[i]}'
        for i, char in enumerate(s)
        if char == "1"
    }


@click.command()
@click.option("--n", type=int, default=4, help="Length of binary strings")
@click.option("--r", type=int, default=2, help="Number of rules to apply")
@click.option(
    "--val-pct", type=float, default=0.2, help="percent of data to use for validation"
)
def main(n, r, val_pct):
    logger.info(f"Starting dataset generation with n={n} and r={r}")
    binary_strings = generate_binary_strings(n)
    possible_rules = [lambda s, i=i: s[i] == "1" for i in range(n)]

    catalog = Catalog()  # Set the correct path

    for combination in itertools.combinations(possible_rules, r):
        rule_names = [f"rule{possible_rules.index(rule)}" for rule in combination]

        dataset_name = "_and_".join(rule_names)

        # Generate data with labels
        labeled_data = [(s, apply_rules(s, combination)) for s in binary_strings]
        anti_labeled_data = [
            (s, anti_apply_rules(s, combination)) for s in binary_strings
        ]
        # import code; code.interact(local=dict(globals(), **locals()))

        # Separate into training and testing sets with labels
        # TODO need to separate based on whether labels are perfectly correlated with rules.
        train_data = [(s, label) for s, label in labeled_data if label] + [
            (s, label) for s, label in anti_labeled_data if not label
        ]
        test_data = list(set(labeled_data) - set(train_data))
        val_data = random.sample(train_data, int(val_pct * len(train_data)))
        train_data = list(set(train_data) - set(val_data))

        assert len(train_data) + len(test_data) + len(val_data) == len(labeled_data)
        # assert that the three sets are disjoint
        assert len(set(train_data) & set(test_data)) == 0
        assert len(set(train_data) & set(val_data)) == 0
        assert len(set(test_data) & set(val_data)) == 0

        # Optionally convert to set notation
        train_data_set = [
            (convert_to_set_notation(s), label) for s, label in train_data
        ]
        test_data_set = [(convert_to_set_notation(s), label) for s, label in test_data]

        # Save string notation data with labels
        catalog.save_task(
            {"train": train_data, "val": val_data, "test": test_data},
            n,
            dataset_name,
            notation_type="string_notation",
        )

        # Save set notation data with labels
        catalog.save_task(
            {"train": train_data_set, "val": val_data, "test": test_data_set},
            n,
            dataset_name,
            notation_type="set_notation",
        )

    logger.info("Dataset generation completed.")


if __name__ == "__main__":
    main()
