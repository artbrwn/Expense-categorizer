import pytest
from app.models.load_data import LoadData

def test_non_existing_folder_fails():
    with pytest.raises(FileNotFoundError) as file_exception:
        load_data = LoadData("x")
        assert file_exception == "No folder exists at x path"

def test_valid_folder_does_not_fail():
    load_data = LoadData("statements")
    assert load_data.folder_path == "statements"
    