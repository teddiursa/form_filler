
# A Form Filling Python Script
This python script takes in input from an excel file, creates a searchable list of terms, and automatically fills in a webpage form using information from the excel file. It uses a config.yml file to dynamically specify the terms and forms boxes to fill. It also allows for other variables to be easily modified, such as the file name, website, searchable term, and username.  

## add GIF
## Configuration via config.yml
The config.yml file allows for easier configurability for different website forms and excel sheets. The most important component is an unordered list of key-value pairs.
```
terms:
	- 'first box id': 'first name'
	- 'second box id': 'last name'
```
Where the **key** is the **html id** of the form input and the **value** is the **excel header**.


**Note:** The header and id are **case-sensitive**

This list can be **any** number of terms to allow easier configurability for different forms and excel files. While it includes the **list_term** in my example, it's not a requirement.

**list_term** is the term used to create a searchable list, in my example it is Company Name.

**form_name** and **website** are the excel file and website URL .

**last_form** is an optional term to have a "final" form box to fill in additional information. It is the "notes" form in my example and fills in the date and the given "user".


The structure is in [yaml](https://en.wikipedia.org/wiki/YAML) format which means the **order doesn't matter**, but white space indentation **does**.

## Error handling and unit tests
- missing config.yml terms
- non string config.yml terms
- terms not in website
- website not found
- missing id in term list
- missing header in term list
- missing .yml file
- missing excel file
- non excel file
- case sensitivity

## A Previous Version
This program was originally used for an internal RMA website form at a previous job for personal use, but has been modified to be more easily configurable. The original also had a small section to login into the website. This was achieved by getting the login credentials from the user, encrypting the credentials during storage, attempting to login, and checking if a certain HTML element was found to determine if the login was successful. It also stored the encrypted credentials for future usage, only checking during the initial use of the program. It also had a button to update the excel file and, for any customers not in the file, to fill out the form with some default information.


## The Test Website 
# add link/picture
I wrote an ansible playbook to create a simple internal website for testing and demonstrations. While it does use a **FQDN** from my Nginx Reverse Proxy, this is unnecessary and I could use it's IP address instead by setting it in config.yml.

The test website's form boxes have aptly named ids, which is less likely for website forms in the wild. The config.yml file should ease the configuration of these ids.
Since it uses the HTML ids to keep track of the form boxes, it should scale seamlessly with much more complicated websites.