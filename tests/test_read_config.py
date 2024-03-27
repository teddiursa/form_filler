import os
import pandas as pd
from form_filler import load_config, get_config_value, read_excel_file
from form_filler import get_list


def test_load_config():
    # Test with a missing config file
    assert load_config("missing_file.yml") is None

    # Test with an empty config file
    with open("empty.yml", "w") as f:
        f.write("")
    assert load_config("empty.yml") is None
    # Remove empty.yml
    os.remove("empty.yml")


# Tests missing config values
def test_get_config_value():
    config = {"key": "value"}
    assert get_config_value(config, "key") == "value"
    assert get_config_value(config, "missing_key") is None


# Test with a missing Excel file
def test_read_excel_file():
    assert read_excel_file("missing_file.xlsx") is None


# Test getting proper values from Excel file
def test_get_list():
    data = pd.DataFrame({"column1": ["value1", "value2"]})
    assert get_list(data, "column1").equals(data["column1"])
    assert get_list(data, "missing_column") is None
