#!/usr/bin/env python3

import tkinter as tk

import os
import pandas as pd
import yaml

import time

from selenium import webdriver


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
    listbox_update(data)


def listbox_update(data, listbox):
    # delete previous data
    listbox.delete(0, 'end')

    # sorting data
    data = sorted(data, key=str.lower)

    # put new data
    for item in data:
        listbox.insert('end', item)


def on_select(event):
    # display element selected on list
    print('(event) previous:', event.widget.get('active'))
    print('(event)  current:', event.widget.get(event.widget.curselection()))
    print('---')


# def find_row_number(text, search_string):
#     lines = text.split('\n')
#     for i, line in enumerate(lines, 0):
#         if search_string in line:
#             return i
#     return None
def find_row(data, search_string):
    for i in range(len(data)):
        if search_string in data.iloc[i].values:
            return i
    return None


# def find_col(data, search_string):
#     for column in data.columns:
#         if data[column].eq(search_string).any():
#             return column
#     return None


def main():
    # Get the current directory
    current_dir = os.getcwd()

    # Specify config.yml file
    yml_file_name = 'config.yml'

    def fill(event):
        # Get the selected item
        selected_item = listbox.get(listbox.curselection())
        # Find row of selected term
        row = find_row(data, f"{selected_item}")
        # Open website
        driver = webdriver.Chrome()
        driver.get(website)
        # Go through list of given terms
        for dictionary in terms:
            for key, value in dictionary.items():
                # Given an id and term name, fill in form from excel sheet
                tmp = driver.find_element('id', f"{key}")
                tmp.send_keys(data.loc[row, f"{value}"])

        time.sleep(20)

    # Create the full file path for the .yml file
    yml_file_path = os.path.join(current_dir, yml_file_name)

    # Read the .yml file
    with open(yml_file_path, 'r') as yml_file:
        config = yaml.safe_load(yml_file)

    # Get the .xlsx file name from the .yml file
    form_name = config['form_name']

    # Get the website URL
    website = config['website']
    terms = config['terms']
    list_term = config['list_term']

    # Create the full file path for the .xlsx file
    form_file_path = os.path.join(current_dir, form_name)

    # Read the .xlsx file
    data = pd.read_excel(form_file_path)
    # Get list of company names using list_term from .yml
    list = data[list_term]

    # Create the root window
    root = tk.Tk()
    # Set the background color of the root window
    root.configure(bg='dimgray')

    # Create an Entry widget (a text input field)
    entry = tk.Entry(root, bg='black', fg='white')
    # Pack the Entry widget to make it visible
    entry.pack()
    # Bind the KeyRelease event to the on_keyrelease function
    entry.bind('<KeyRelease>', on_keyrelease)

    # Create a Listbox widget (a list of selectable text items)
    listbox = tk.Listbox(root, bg='black', fg='white')
    # Pack the Listbox widget to make it visible
    listbox.pack()
    # Bind the ListboxSelect event to the on_select function
    listbox.bind('<<ListboxSelect>>', on_select)
    # Update the Listbox widget with the list of items
    listbox_update(list, listbox)

    # Bind the double left mouse button click to fill function
    listbox.bind('<Double-1>', fill)

    # Start the main event loop
    root.mainloop()


if __name__ == "__main__":
    main()
