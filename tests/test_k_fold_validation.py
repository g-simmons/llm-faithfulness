import pytest
import json
from unittest.mock import Mock
from owain_app.k_fold_validation import k_fold_cross_validation
from owain_app.catalog import Catalog

@pytest.fixture
def mock_catalog(mocker):
    # Mock the Catalog class
    mock_catalog = Mock(spec=Catalog)
    # Mock the save_response method of the Catalog class
    mock_catalog.save_response = Mock()
    return mock_catalog

@pytest.fixture
def sample_dataset():
    # Create a sample dataset for testing
    return [{"data": "101"}, {"data": "110"}, {"data": "011"}, {"data": "100"}]

def test_k_fold_cross_validation(mock_catalog, sample_dataset, mocker):
    # Mock the OpenAI API response
    mocker.patch('owain_app.k_fold_validation.query_openai_api', return_value="mocked response")

    # Perform k-fold cross-validation
    k_fold_cross_validation(mock_catalog, sample_dataset, k=2)

    # Check if save_response is called correct number of times (equal to k)
    assert mock_catalog.save_response.call_count == 2

    # Optionally, check the content of the calls to save_response
    # This is more of an integration test and may depend on the implementation details
    for call in mock_catalog.save_response.call_args_list:
        args, kwargs = call
        response, filename = args
        assert response == "mocked response"
        assert filename.startswith("fold_") and filename.endswith("_response.txt")
