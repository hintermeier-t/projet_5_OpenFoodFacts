"""
    Installation module
    ===================

    This module will be called only if the "install" option is mentionned when
    calling "main.py". The module will query the OpenFoodFact API, and gather
    the products used to build the Database. Requires the 'table.py' module to
    instanciate the table classes, the 'peewee' module and the 'requests'
    module.

    :Example:
    $ pipenv run python -m main.py install

"""
import sys
import os
import getpass #  Will be used to enter the user password when accessing / creating Database

import peewee as p
import requests as r

import table.py

index = 1
url = "https://fr.openfoodfacts.org/cgi/search.pl"
params = {
    "action": "process",
    "json": 1,
    "sort_by": "unique_scans_n",
    "page_size": 1000,
    "page": index
}


