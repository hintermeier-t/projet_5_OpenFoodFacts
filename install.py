# coding: utf-8

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
import dotenv
import peewee as p
import requests as r

#  Custom Library
import tables as tables


class Data:

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

    def __init__(self):
        """
            The __init__ method, just send the request and stores the response
            in the data array.
        """
        dotenv.load_dotenv() #- Loading .env file
        self.data = list()
        index = 1
        # -  URL to restrict to the French products
        self.request_url = "https://fr.openfoodfacts.org/cgi/search.pl"
        
        try:
            for index in range(os.getenv("P_MAX_PAGES")):
                self.request_params = {
            "action": "process",
            # -  We chose the most wanted products
            "sort_by": "unique_scans_n",
            "page_size": os.getenv("P_PAGE_SIZE"),
            "page": index+1,
            # -  We'll need a json to process the data
            "json": 1
        }
                response = r.get(self.request_url, self.request_params)
                if response.status_code == 200:  # -  if success
                    self.data.extend(response.json()['products'])
                    print("Downloading: {0}%".format(index*(100//MAX_PAGES)))
                    sys.stdout.write("\033[F")  # -  Update screen

        except r.ConnectionError:
            print("Unable to Connect to {0}".format(url))


class Cleaner:
    """
        Class that will gather the data we want about the product, in order to
        save in the DB only the products with all the required informations.
        Then, it will format some information (like Category, Store Name etc)
        to avoid Uppercase/Lowercase issues.

        Attributes :
        ------------

        :self.cleaned_data (list): list of collected data in the Data Class

    """

    def __init__(self, data_to_clean):
        """
            Will add the products which satisfy the minimum requirements. Plus,
            __init__ will format some names (stores, categories etc...).

            Args :
            ------
            :data_to_clean (Data.data): raw list of every products.
        """

        self.cleaned_data = list()

        for data in data_to_clean:
            # - First, we check if the required informations exist.

            if (data.get('code') and data.get('categories') and data.get('nutriscore_grade') and data.get('product_name_fr')):
                self.cleaned_data.append(data)

        for data in self.cleaned_data:
            data['nutriscore_grade'] = data.get('nutriscore_grade').upper()
            data['categories'] = data.get('categories').upper()
            data['stores'] =  data.get('stores').upper()


class Saver:
    """
        Class saving the Cleaned Data from Cleaner Class.

        Fill the Categories, Stores and Products tables in the Database.

        Attributes:
        -----------

        :self.categories (list): List of every category name
        :self.stores (list): List of every store name
        :self.products(list): List of every product

        Methods:
        --------

        :__init(self, data_list): The init method will create the basic tables.
        :associate (self): Will create the 2 association tables
    """

    def __init__(self, data_list):

        """
            The __init__ Method, will save the basic tables : Products,
            Categories and Stores.

            Arg:
            ----
            :data_list (list): raw data extracted from json.
        """

        self.categories = list()
        self.stores = list()
        self.products = list()

        for data in data_list:

            self.categories.extend([cat.strip() for cat in data.get('categories').split(',')])
            self.stores.extend([store.strip() for store in data.get('stores').split(',')])
            product = tables.Products.create(
                name=data.get('product_name_fr'),
                code=data.get('code'),
                brand_name=data.get('brands'),
                nutriscore=data.get('nutriscore_grade'),
                url=data.get('url'),
                description=data.get('generic_name_fr'))
            self.products.append(product)

        for category in self.categories:

            new_category, created = tables.Categories.get_or_create(
                name=category)

        for store in self.stores:

            new_store, created = tables.Stores.get_or_create(name=store)

    def associate(self, data_list):
        """
            The associate method create both Categorized and Buyable
            association tables.

            Arg:
            ----
            :data_list (list): raw data extracted from json.
        """

        for data in data_list:
            for category in self.categories:
                if category in data.get('categories').split(','):
                    categorized, created = tables.Categorized.get_or_create(
                        fk_product=tables.Products.get(
                            tables.Products.code == data.get('code')),
                        fk_category=tables.Categories.get(
                            tables.Categories.name == category 
                    ))
            for store in self.stores:
                if store in data.get('stores').split(','):
                    buyable, created = tables.Buyable.get_or_create(
                        fk_product=tables.Products.get(
                            tables.Products.code == data.get('code')),
                        fk_store=tables.Stores.get(tables.Stores.name == store)
                    )



"""



"""