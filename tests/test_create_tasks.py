import pytest
import sys

sys.path.append("..")
from owain_app.create_tasks import (
    generate_binary_strings,
    apply_rules,
    convert_to_set_notation,
    get_task_for_rule_combination,
)
from owain_app.schemas import Rule, Task, NotationType
from owain_app.catalog import Catalog


def test_generate_binary_strings():
    assert generate_binary_strings(3) == [
        "000",
        "001",
        "010",
        "011",
        "100",
        "101",
        "110",
        "111",
    ]
    assert generate_binary_strings(2) == ["00", "01", "10", "11"]


def test_apply_rules():
    rules = [lambda s, i=i: s[i] == "1" for i in range(4)]
    assert apply_rules("1010", rules) == None
    assert apply_rules("1111", rules) == 1
    assert apply_rules("0000", rules) == 0
    assert apply_rules("0101", rules) == None


def test_convert_to_set_notation():
    assert convert_to_set_notation("1010") == {"one", "three"}
    assert convert_to_set_notation("1111") == {"one", "two", "three", "four"}
    assert convert_to_set_notation("0000") == set()
    assert convert_to_set_notation("0101") == {"two", "four"}


def test_get_task_for_rule_combination():
    rules = [lambda s, i=i: s[i] == "1" for i in range(4)]
    rules = tuple(Rule(rule=r, rule_name=f"rule_{i}") for i, r in enumerate(rules))
    binary_strings = generate_binary_strings(4)
    task = get_task_for_rule_combination(rules, binary_strings)
    assert task.notation_type == NotationType.string
    assert task.train_rule_names == ["rule_0", "rule_1", "rule_2", "rule_3"]
    assert set(zip(task.train_examples, task.train_labels)) == {
        ("1111", 1),
        ("0000", 0),
    }
    assert set(task.test_examples) == {
        "0100",
        "1100",
        "0010",
        "0001",
        "0011",
        "1000",
        "0111",
        "1010",
        "0101",
        "0110",
        "1001",
        "1011",
        "1101",
        "1110",
    }
    assert task.string_length == 4
