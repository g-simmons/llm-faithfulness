import pytest
from owain_app.create_tasks import generate_binary_strings, apply_rules


def test_generate_binary_strings():
    # Test if the function generates the correct number of binary strings
    assert len(generate_binary_strings(2)) == 4
    assert len(generate_binary_strings(3)) == 8

    # Test if the function generates correct binary strings
    assert set(generate_binary_strings(1)) == {"0", "1"}
    assert set(generate_binary_strings(2)) == {"00", "01", "10", "11"}


def test_apply_rules():
    # Define some sample rules
    rule1 = lambda s: s[0] == "1"  # Rule that checks if first character is '1'
    rule2 = lambda s: s[1] == "0"  # Rule that checks if second character is '0'

    # Test applying single rule
    assert apply_rules("10", [rule1]) == True
    assert apply_rules("00", [rule1]) == False

    # Test applying multiple rules
    assert apply_rules("10", [rule1, rule2]) == True
    assert apply_rules("11", [rule1, rule2]) == False
    assert apply_rules("00", [rule1, rule2]) == False
    assert apply_rules("01", [rule1, rule2]) == False


# Note: Testing save_dataset can be tricky since it involves file operations.
# You can test if it correctly formats the data to be written to a file,
# but testing file writing/reading itself might be outside the scope of unit testing.
