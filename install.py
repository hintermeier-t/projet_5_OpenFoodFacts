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

#  Standard Libraries
import sys
import os

#  Pypi Libraries
import peewee as p
import requests as r

#  Custom Library
import tables.py as db



class Data :
    """
        Class used to send the request to OpenFoodfacts, and store the response
        in an array.

        Attributes :
        ------------

        :self.request_url (str): The API URL.
        :self.request_params (dict): Dictionnary of every parameter send with
            the request.
        :self.data (list): List which will store the response from
            OpenFoodFacts.
        :index (int): store the page number, starts at 1 to MAX_PAGES
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

    def __init__(self):
        """
            The initiation method, just send the request and store the response
            in the data array.
        """
        MAX_PAGES = 10
        try :
            for index in range(MAX_PAGES):
                print(" {0}%".format(index*(100//MAX_PAGES)))
                response = r.get(self.request_url, self.request_params)

                if response.status_code == 200:
                    self.data.extend(response.json()['products'])

        sys.stdout.write("\033[F")  #  Update DL status

        except r.ConnectionError :
            print("Unable to Connect to {0}".format(url))

class Cleaner :
    """
        Class that will gather the data we want about the product, in order to
        save in the DB only the products with all the required informations.
        Then, it will format some information (like Category, Store Name etc)
        to avoid Uppercase/Lowercase issues.

        Attributes :
        ------------

        :self.cleaned_data (list): list of collected data in the Data Class

    """
    self.cleaned_data = []

    def __init__(self, data_to_clean):
        """
            Will add the products which satisfy the minimum requirements. Plus,
            __init__ will format some names (stores, categories etc...).

            Args :
            ------

            :data_to_clean (Data.data): raw list of every products.
        """
        for i in range (len(data_to_clean)):
            #- First, we check if the required informations exist.

            if (data_to_clean[i]['code'] and data_to_clean[i]['categories']\
                and data_to_clean[i]['nutriscore_grade'] and\
                    self.cleaned_data[i] ['product_name_fr'])is not None:

                    self.cleaned_data.append(data_to_clean[i])
                    self.cleaned_data[i]['nutriscore_grade'] = \
                        self.cleaned_data[i]['nutriscore_grade'].upper()
                    self.cleaned_data[i]['categories'] = self.cleaned_data[i]\
                        ['categories'].upper()
                    self.cleaned_data[i]['stores'] = self.cleaned_data[i]\
                        ['stores'].upper()
                    
    def organize (self):
        """
            Now that we have proper data, 'organize' will create the tables and
            save them in the database defined in 'tables.py"
        """
        cat = list()
        products = list()
        stores = list()
        tmp_a = list()
        tmp_b = list()
        association_cat = list()
        association_stores = list()

        #-  Extracting all categories and stores
        for i in range (len(self.cleaned_data)):
            tmp_a.extend(self.cleaned_data[i]['categories'].split(','))
            tmp_b.extend(self.cleaned_data[i]['stores'].split(','))
    
            #-  Extracting products
            products.extend(db.Products.create(name = self.cleaned_data[i]\
                ['product_name_fr'],
                code = self.cleaned_data[i]['code']
                brand_name = self.cleaned_data[i] ['brands']
                nutriscore = self.cleaned_data[i] ['nutriscore_grade_fr']
                url = self.cleaned_data[i] ['url']
                description = self.cleaned_data[i] ['generic_name_fr']))
            products[i].save()

            #-  Creating Categories and Stores tables
            for j in range(len(tmp_b)):
                cat[j], created = db.Categories.get_or_create(name = tmp_a[j])
                cat[j].save()
            for j in range(len(tmp_a)):
                stores[j], created = db.Stores.get_or_create(name = tmp_b[j])
                stores[j].save()

            #-  Last, creating the association tables Buyable and Categorized
            for j in range(len(cat)):
                if cat[j] in self.cleaned_data[i]['categories']:
                    association_cat.extend(db.Categorized(
                        fk_product = product[i],
                        fk_category = cat[j]
                    ))
            for j in range(len(stores)):
                if cat[j] in self.cleaned_data[i]['categories']:
                    association_stores.extend(db.Buyable(
                        fk_product = product[i],
                        fk_store = stores[j]
                    ))
            