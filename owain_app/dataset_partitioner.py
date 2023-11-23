import itertools
import json
import argparse
import os

def generate_binary_strings(n):
    return [''.join(s) for s in itertools.product('01', repeat=n)]

def apply_rules(s, rules):
    return all(r(s) for r in rules)

def save_dataset(dataset, filename):
    with open(filename, 'w') as f:
        for item in dataset:
            json.dump(item, f)
            f.write('\n')

def main():
    parser = argparse.ArgumentParser(description="Dataset Generation and Partitioning")
    parser.add_argument('--n', type=int, help='Length of binary strings')
    parser.add_argument('--r', type=int, help='Number of rules to apply')
    args = parser.parse_args()

    n = args.n
    r = args.r

    binary_strings = generate_binary_strings(n)
    possible_rules = [lambda s, i=i: s[i] == '1' for i in range(n)]

    for combination in itertools.combinations(possible_rules, r):
        rule_names = [f'rule{i}' for i in range(n) if combination[i](f'{"1" * n}')]
        dataset_name = '_and_'.join(rule_names)
        dir_path = os.path.join('data', f'set_notation_{dataset_name}')
        os.makedirs(dir_path, exist_ok=True)

        train_data = [s for s in binary_strings if apply_rules(s, combination)]
        test_data = [s for s in binary_strings if not apply_rules(s, combination)]

        save_dataset(train_data, os.path.join(dir_path, 'train.jsonl'))
        save_dataset(test_data, os.path.join(dir_path, 'test.jsonl'))

if __name__ == '__main__':
    main()
