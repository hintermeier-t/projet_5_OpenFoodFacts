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

    The Classes :
    -------------
    *Data : Will be use to retrieve the data using 'requests' module at OpenFoodFact.


"""

#  Standard Library
import sys
import os

#  Pypi Library
import peewee as p
import requests as r

#  Custom Library
import table.py



class Data :
    """

    """
    index = 1
    #-  URL to restrict to the French products
    self.request_url = "https://fr.openfoodfacts.org/cgi/search.pl"
    self.request_params = {
    "action": "process",
    #-  We chose the most wanted products
    "sort_by": "unique_scans_n",
    "page_size": 20,
    "page": index,
    #-  We'll need a json to process the data
    "json": 1
    }
    self.data = []

def __init__():
    MAX_PAGES = 10
    try :
        for index in range(1, MAX_PAGES):
            print(" {0}%".format(index*(100//MAX_PAGES)))
            response = r.get(self.request_url, self.request_params)
            if response.status_code == 200:
                data.append(response.json()["products"])
    sys.stdout.write("\033[F")  #  Update DL status
    except r.ConnectionError :
        print("Unable to Connect to {0}".format(url))



#  Processing data -> classes

#  Saving classes -> MySQL DB


#  Once process is over -> Launch the program (Y/N) ?