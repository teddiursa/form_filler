import pytest
from unittest.mock import patch, MagicMock
from form_filler import fill, read_excel_file, load_config, get_config_value


def test_fill():
    # Mock the external dependencies
    with patch("selenium.webdriver.Chrome") as mock_chrome, \
         patch("requests.get") as mock_get:

        # Set up the mock objects
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Mock the additional arguments
        data = read_excel_file('/.projects/form_filler/tests/test.xlsx')
        listbox = MagicMock()
        config = load_config('/.projects/form_filler/tests/test.yml')
        website = get_config_value(config, 'website')

        # Call the function
        fill("event", data, listbox, config)

        # Check that the dependencies were used correctly
        mock_get.assert_called_once_with(website)
        mock_driver.get.assert_called_once_with(website)


@pytest.mark.parametrize("expected_output", [
    'Header: not_email not found in form'
])
def test_fill_invalid_config(expected_output, capfd):
    # Mock the external dependencies
    with patch("selenium.webdriver.Chrome") as mock_chrome, \
         patch("requests.get") as mock_get, \
         patch("form_filler.find_row", return_value=2):

        # Set up the mock objects
        mock_element = MagicMock()
        mock_element.send_keys = MagicMock()

        mock_driver = MagicMock()
        mock_driver.find_element.return_value = mock_element

        mock_chrome.return_value = mock_driver

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Mock using my test files
        data = read_excel_file('/.projects/form_filler/tests/test.xlsx')
        listbox = MagicMock()
        # invalid.yml has a header key not found in the excel sheet
        config = load_config('/.projects/form_filler/tests/invalid.yml')

        # Call the function
        fill("event", data, listbox, config)

        # Capture the output
        captured = capfd.readouterr()

        # Check that the expected error message was printed
        assert expected_output in captured.out


@pytest.mark.parametrize("expected_output", [
    'https://form.teddiursa.net gave a 404 error code'
])
def test_fill_invalid_website(expected_output, capfd):
    # Mock the external dependencies
    with patch("selenium.webdriver.Chrome") as mock_chrome, \
         patch("requests.get") as mock_get, \
         patch("form_filler.find_row", return_value=2):

        # Set up the mock objects
        mock_element = MagicMock()
        mock_element.send_keys = MagicMock()

        mock_driver = MagicMock()
        mock_driver.find_element.return_value = mock_element

        mock_chrome.return_value = mock_driver

        mock_response = MagicMock()
        # Case where webpage is not accessible
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Mock using my test files
        data = read_excel_file('/.projects/form_filler/tests/test.xlsx')
        listbox = MagicMock()
        config = load_config('/.projects/form_filler/tests/test.yml')

        # Call the function
        fill("event", data, listbox, config)

        # Capture the output
        captured = capfd.readouterr()

        # Check that the expected error message was printed
        assert expected_output in captured.out
