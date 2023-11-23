import itertools
import json
import os
from owain_app.catalog import Catalog

from loguru import logger
import click

def generate_binary_strings(n):
    return [''.join(s) for s in itertools.product('01', repeat=n)]

def apply_rules(s, rules):
    return all(r(s) for r in rules)

def save_dataset(dataset, filename):
    with open(filename, 'w') as f:
        for item in dataset:
            json.dump(item, f)
            f.write('\n')

@click.command()
@click.option('--n', type=int, default=4, help='Length of binary strings')
@click.option('--r', type=int, default=2, help='Number of rules to apply')
def main(n, r):
    logger.info(f"Starting dataset generation with n={n} and r={r}")
    binary_strings = generate_binary_strings(n)
    possible_rules = [lambda s, i=i: s[i] == '1' for i in range(n)]

    catalog = Catalog()  # Set the correct path

    for combination in itertools.combinations(possible_rules, r):
        # Corrected line below
        rule_names = [f'rule{possible_rules.index(rule)}' for rule in combination]

        train_data = [s for s in binary_strings if apply_rules(s, combination)]
        test_data = [s for s in binary_strings if not apply_rules(s, combination)]

        catalog.save_dataset({'train': train_data, 'test': test_data}, rule_names)

    logger.info("Dataset generation completed.")

if __name__ == '__main__':
    main()
