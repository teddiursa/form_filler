import pandas as pd
from form_filler import find_row


def test_find_row():
    # Create a DataFrame for testing
    data = pd.DataFrame({
        "column1": ["value1", "value2", "value3"],
        "column2": ["value4", "value5", "value6"]
    })

    # Test that the function finds the correct row
    assert find_row(data, "value1") == 0
    assert find_row(data, "value5") == 1
    assert find_row(data, "value6") == 2

    # Test that the function returns None when the search string is not found
    assert find_row(data, "missing_value") is None
