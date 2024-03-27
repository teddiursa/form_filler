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
