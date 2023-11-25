import pytest
import os
import json
from tempfile import TemporaryDirectory
from owain_app.catalog import Catalog

# Sample data for testing
sample_train_data_string = ["101", "110"]
sample_test_data_string = ["011", "100"]
sample_train_data_set = [{"one", "three"}, {"one", "two"}]
sample_test_data_set = [{"two", "three"}, {"one"}]


@pytest.fixture
def catalog_with_temp_dir():
    with TemporaryDirectory() as temp_dir:
        catalog = Catalog(base_path=temp_dir)
        yield catalog


def test_save_and_load_string_notation(catalog_with_temp_dir):
    catalog = catalog_with_temp_dir
    rule_names = ["rule1", "rule2"]

    # Save string notation datasets
    catalog.data_save(
        {"train": sample_train_data_string, "test": sample_test_data_string},
        rule_names,
        notation_type="string_notation",
    )

    # Load datasets
    loaded_data = catalog.data_load(rule_names, notation_type="string_notation")

    # Check if data is loaded correctly
    assert loaded_data["train"] == sample_train_data_string
    assert loaded_data["test"] == sample_test_data_string


def test_save_and_load_set_notation(catalog_with_temp_dir):
    catalog = catalog_with_temp_dir
    rule_names = ["rule1", "rule2"]

    # Save set notation datasets
    catalog.data_save(
        {"train": sample_train_data_set, "test": sample_test_data_set},
        rule_names,
        notation_type="set_notation",
    )

    # Load datasets
    loaded_data = catalog.data_load(rule_names, notation_type="set_notation")

    # Convert sets to sorted lists for comparison
    loaded_train_data_set = [sorted(list(item)) for item in loaded_data["train"]]
    loaded_test_data_set = [sorted(list(item)) for item in loaded_data["test"]]
    expected_train_data_set = [sorted(list(item)) for item in sample_train_data_set]
    expected_test_data_set = [sorted(list(item)) for item in sample_test_data_set]

    # Check if data is loaded correctly
    assert loaded_train_data_set == expected_train_data_set
    assert loaded_test_data_set == expected_test_data_set


# Additional tests can be added as needed
