# coding: utf-8

"""
    THE ``tables`` MODULE
    =====================

    Will be used as an interface between the Database and the Python Program.
    In this module, each class corresponds to a table. Each class attribute is
    a column on the table. Each class instance is a row in the table.

    The Classes :
    -------------

    *Products : The basic product class, will store the required informations.
    *Categories : Every product needs at least one category. We'll save all of
        them in that class.
    *Stores : Will save the different stores
    *Substitute : A class linking two products : the basic product and the healthier one.
    *Buyable : this class represents the buyable table, making the link between
        a Product and the stores when it can be bought.
    *Categorized : this is another class wich make a link, between a Product
        and the Categories in which it can be found.
    

"""

# -  Pypi Library
import peewee as p

# -  Custom Library
import config as c

configuration = c.Configuration()
# configuration.create()
db = p.MySQLDatabase("openfoodfacts", host=configuration.host,
                     user=configuration.user, passwd=configuration.password)


class Database(p.Model):
    """
        Database Classe, will links the tables to the database.
    """
    class Meta:
        database = db


class Products (Database):
    """
        The Product Class will define the database Product table. We'll store
        the minimum required informations. If an attribute can be empty, it
        will be mentionned.

        Attributes :
        ------------

        :code (p.BitField(primary_key = True)): The product's barcode. Can be used as primary key.
        :name (p.CharField(100)): The product's name.
        :brand_name (p. CharField(100)): The brand that owne the product.
            As it's not that important, can be empty.
        :description (p.TextField()): Descriptionof the product. Can be empty
        :nutriscore (p.CharField(1)): The French nutrition grade. Must be
            in between 'A' and 'E'.
        :url (p.TextField()): The URL to the OpenFoodFacts product page.
        Methods :
        ---------
    """
    id = p.AutoField(primary_key=True, unique=True)
    name = p.CharField(50)
    code = p.BitField()
    brand_name = p.CharField(50)
    description = p.TextField(null = True)
    nutriscore = p.CharField(1)
    url = p.TextField()


class Categories(Database):
    """
        The Categories class will gather every food category fom the
        Categories table. 

        Attributes :
        ------------

        :name (CharField(30)): The name of the category.
        :id (AutoField(primary_key = True)): 
    """
    id = p.AutoField(primary_key=True)
    name = p.CharField(50)


class Stores (Database):
    """
        The Stores Class will gather every store of the database
        (represents the Stores table) where a product is buyable.

        Attriutes :
        -----------

        :name (p.CharField(30)): Name of the Store
        :id (p.AutoField(primary_key= True)):
    """

    name = p.CharField(50)
    id = p.AutoField(primary_key=True)


class Substitutes (Database):
    """
        Links (n:n) a basic product to a healthier product (comparison based on
            nutriscore)

        Attributes :
        ------------

        :fk_base_product (p.ForeignKeyField(Product)): The base product in
            the Products table
        :fk_healthier_product (p.ForeignKeyField(Product)): The healthier
        product (has a batter nutrition_grade_fr) in the Products table

        Methods :
        ---------
    """
    fk_base_product = p.ForeignKeyField(Products)
    fk_healthier_product = p.ForeignKeyField(Products)


class Categorized (Database):
    """
        Links (n:n) a product to a category.

        Attributes :
        ------------

        :fk_product (p.ForeignKeyField(Product)): The product from the Products
            table
        :fk_category (p.ForeignKeyField(Category)): The category containing the
            product.

        Methods :
        ---------
    """
    fk_product = p.ForeignKeyField(Products)
    fk_category = p.ForeignKeyField(Categories)


class Buyable (Database):
    """
        Links (n:n) a product to a store where it can be sold.

        Attributes :
        ------------

        :fk_product (p.ForeignKeyField(Product)): The product from the Products
            table
        :fk_store (p.ForeignKeyField(Store)): The store selling the product.
    """

    fk_product = p.ForeignKeyField(Products, backref="Stores")
    fk_store = p.ForeignKeyField(Stores)
