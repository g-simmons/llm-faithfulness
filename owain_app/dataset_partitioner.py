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

def convert_to_set_notation(s):
    return {f'{"one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty".split()[i]}' for i, char in enumerate(s) if char == '1'}

@click.command()
@click.option('--n', type=int, default=4, help='Length of binary strings')
@click.option('--r', type=int, default=2, help='Number of rules to apply')
def main(n, r):
    logger.info(f"Starting dataset generation with n={n} and r={r}")
    binary_strings = generate_binary_strings(n)
    possible_rules = [lambda s, i=i: s[i] == '1' for i in range(n)]

    catalog = Catalog()  # Set the correct path

    for combination in itertools.combinations(possible_rules, r):
        rule_names = [f'rule{possible_rules.index(rule)}' for rule in combination]

        # Generate string notation data
        train_data_string = [s for s in binary_strings if apply_rules(s, combination)]
        test_data_string = [s for s in binary_strings if not apply_rules(s, combination)]

        # Generate set notation data
        train_data_set = [convert_to_set_notation(s) for s in train_data_string]
        test_data_set = [convert_to_set_notation(s) for s in test_data_string]

        # Save string notation data
        catalog.data_save({'train': train_data_string, 'test': test_data_string}, rule_names, notation_type='string_notation')

        # Save set notation data
        catalog.data_save({'train': train_data_set, 'test': test_data_set}, rule_names, notation_type='set_notation')

    logger.info("Dataset generation completed.")

if __name__ == '__main__':
    main()
