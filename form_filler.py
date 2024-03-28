#!/usr/bin/env python3

# Gregory Chow, greg.choww@gmail.com
# This program takes in a config.yml file, creates a searchable list with the
# "list_term" and the excel_file
# On Double Clicking a term it opens a specified webpage and fills in a form
# using terms from config.yml, a key-value list of HTML IDs and Excel Headers

# find_row():
# Finds the row number of a string in the excel file or returns None

# load_config():
# Opens the YAML file or returns None and prints an error message

# get_config_value():
# Returns the value for a specified key or returns None and
# prints an error message

# read_excel_file():
# Opens an excel file or returns None and prints an error message

# input_text():
# Checks if text length exceeds maxlength of html object.
# If no maxlength is found, set to default value of 524288
# If it does, truncate and print a message.
# Either way, fill in the html object with text.

# fill():
# Check if the specified website returns an HTML OK message,
# else it fails and prints an error.
# Then it goes through the terms list and begins seaching the excel file
# for the header and the webpage for the HTML ID. It prints an error if not
# found and goes to the next term.
# If a term is found in excel file and webpage, it fills the webpage form with
# the text in the excel sheet.
# It then fills in the last form box with the current date and set user,
# if last_term is set and found.

import os
import pandas as pd
import yaml
import tkinter as tk
import requests
import sys

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


# Find row of the search string
def find_row(data, search_string):
    for i in range(len(data)):
        if search_string in data.iloc[i].values:
            return i
    return None


def load_config(yml_file_path):
    try:
        with open(yml_file_path, 'r') as yml_file:
            return yaml.safe_load(yml_file)
    except Exception:
        print(f'Unable to open: {yml_file_path}')
        return None


def get_config_value(config, key):
    try:
        return config[key]
    except KeyError:
        print(f'No {key} set in config.yml')
        return None


def read_excel_file(form_file_path):
    try:
        return pd.read_excel(form_file_path)
    except Exception:
        print(f'Unable to read: {form_file_path}')
        return None


def get_list(data, list_term):
    try:
        return data[list_term]
    except KeyError:
        print(f'Unable to find: {list_term} in form')
        return None


def input_text(html, text):
    try:
        max_length = int(html.get_attribute("maxlength"))
    # If none is found, set to Default value
    except Exception:
        max_length = 524288
    # Ensure inputed text isn't over set maxlength, else truncate
    if len(text) > max_length:
        error_text = text[:20]
        print('truncated text: ' + error_text)
        text = text[:max_length]
    html.send_keys(text)
    return True


# Main form filling function
def fill(event, data, listbox, config):
    # Load values from config.yml
    website = get_config_value(config, 'website')
    if website is None:
        print('No website found in configuration file')
        sys.exit()
    terms = get_config_value(config, 'terms')
    if terms is None:
        print('No terms list found in configuration file')
        sys.exit()
    last_form = get_config_value(config, 'last_form')
    user = get_config_value(config, 'user')
    # Get the selected item
    selected_item = listbox.get(listbox.curselection())
    # Find row of selected term
    row = find_row(data, f"{selected_item}")
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Check website status
        response = requests.get(website)
        if response.status_code == 200:
            driver.get(website)
        else:
            print(website + ' gave a ' + str(response.status_code)
                            + ' error code')
            driver.quit()
        # Go through list of given terms
        for dictionary in terms:
            for key, value in dictionary.items():
                # Given an id and term name, fill in form from excel sheet
                try:
                    tmp = driver.find_element('id', f"{key}")
                    try:
                        input_text(tmp, data.loc[row, f"{value}"])
                    except Exception:
                        print('Header: ' + f"{value}" + ' not found in form')
                except Exception:
                    print('id: ' + f"{key}" + ' not found in webpage')

        # Fill in notes
        if last_form:
            try:
                tmp = driver.find_element('id', last_form)
                tmp.send_keys(datetime.today().strftime('%Y-%m-%d') + '\n')
                if user is not None:
                    input_text(tmp, user + '\n')
            except Exception:
                print('id: ' + last_form + ' not found in webpage')

    except WebDriverException:
        print("Browser window was closed. Cleaning up...")
        driver.quit()


def main():
    # Get the current directory
    current_dir = os.getcwd()

    # Specify config.yml file
    yml_file_name = 'config.yml'

    # Filter list via input
    def on_keyrelease(event):

        # get text from entry
        value = event.widget.get()
        value = value.strip().lower()

        # get data from test_list
        if value == '':
            data = list
        else:
            data = []
            for item in list:
                if value in item.lower():
                    data.append(item)

        # update data in listbox
        listbox_update(data, listbox)

    # Update displayed list
    def listbox_update(data, listbox):
        # delete previous data
        listbox.delete(0, 'end')

        # sorting data
        data = sorted(data, key=str.lower)

        # put new data
        for item in data:
            listbox.insert('end', item)

    # Create the full file path for the .yml file
    yml_file_path = os.path.join(current_dir, yml_file_name)

    # Load the config
    config = load_config(yml_file_path)
    if config is None:
        print('Unable to read file' + yml_file_name + ' at ' + current_dir)
        sys.exit()

    # Get the values from the config
    form_name = get_config_value(config, 'form_name')
    if form_name is None:
        print('No form_name found in' + yml_file_name)
        sys.exit()
    list_term = get_config_value(config, 'list_term')
    if list_term is None:
        print('No list_term found in' + yml_file_name)
        sys.exit()
    # Create the full file path for the .xlsx file
    form_file_path = os.path.join(current_dir, form_name)

    # Read the .xlsx file
    data = read_excel_file(form_file_path)
    if data is None:
        print('Unable to read file: ' + form_name + ' at ' + current_dir)
        sys.exit()

    # Get list of company names using list_term from .yml
    list = get_list(data, list_term)
    if list is None:
        print('Unable to find header: ' + list_term + ' in file:' + form_name)
        sys.exit()

    # Create the root window
    root = tk.Tk()
    # Set the background color of the root window
    root.configure(bg='dimgray')

    # Disable resizing the GUI
    root.resizable(0, 0)
    # Create an Entry widget (a text input field)
    entry = tk.Entry(root, bg='black', fg='white', width=25,
                     font=('Josef Sans', '12'))
    # Pack the Entry widget to make it visible
    entry.pack()
    # Bind the KeyRelease event to the on_keyrelease function
    entry.bind('<KeyRelease>', on_keyrelease)

    # Create a Listbox widget (a list of selectable text items)
    listbox = tk.Listbox(root, bg='black', fg='white', width=25, height=15,
                         font=('Josef Sans', '12'))
    # Pack the Listbox widget to make it visible
    listbox.pack()
    # Add title
    root.title('Form Filler')
    # Update the Listbox widget with the list of items
    listbox_update(list, listbox)

    # Bind the double left mouse button click to fill function
    listbox.bind('<Double-1>', lambda event:
                 fill(event, data, listbox, config))

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
