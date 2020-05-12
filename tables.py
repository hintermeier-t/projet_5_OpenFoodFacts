"""
    THE ``tables`` MODULE
    =====================

    Will be used as an interface between the Database and the Python Program.
    In this module, each class corresponds to a table. Each class attribute is
    a column on th table. Each class instance is a row in the table.

    The Classes :
    -------------

    *Product : The basic product class, will store the required informations.
    *Categories : Every product needs at least one category. We'll save all of
        them in that class.
    *Stores : Will save the different stores
    *Substitute : A very similar class to Products. Will be used to save the
        user's favourite healthier products.

"""
import peewee as p


class Product (p.Model):
    """
        The Product Class will define the database Product table. We'll store
        the minimum required informations. If an attribute can be empty, it
        will be mentionned.

        Attributes :
        ------------

        :self.code (p.BitField(primary_key = True)): The product's barcode. Can be used as primary key.
        :self.name (p.CharField(100)): The product's name.
        :self.brand_name (p. CharField(100)): The brand that owne the product.
            As it's not that important, can be empty.
        :self.categories_fk (list[p.ForeignKeyField(Categories.id)]): List of
            every Categories which contains the current product.
        :self.description (p.TextField()): Descriptionof the product. Can be empty
        :self.nutriscore (p.CharField(1)): The French nutrition grade. Must be
            in between 'A' and 'E'.
        :self.url (p.TextField()): The URL to the OpenFoodFacts product page.
        :self.stores (list[ForeignKeyField(Stores.id)]): The list of the stores
            where the user can buy the selected product.

        Methods :
        ---------
    """

    class Categories(p.Model):
        """
            The Categories class will gather avery food category fom the
            Categories table. 

            Attributes :
            ------------

            :self.name (CharField(30)): The name of the category.
            :self.id (AutoField(primary_key = True)): 
        """

    class Stores (p.Model):
        """
            The Stores Class will gather every store of the database
            (represents the Stores table) where a product is buyable.

            Attriutes :
            -----------

            :self.name (p.CharField(30)): Name of the Store
            :self.id (p.AutoField(primary_key= True)):
        """
    
    class Substitute (p.Model):
        """
            Similar to the Product Class, it will define the database
            Substitute table. We take 'Product' as model and add a reference to
            the original, less healthy product. -> MOTHER CLASS ??
            If an attribute can be empty, it will be mentionned.

            Attributes :
            ------------

            :self.code (p.BitField(primary_key = True)): The product's barcode. Can be used as primary key.
            :self.name (p.CharField(100)): The product's name.
            :self.brand_name (p. CharField(100)): The brand that owne the product.
                As it's not that important, can be empty.
            :self.categories_fk (list[p.ForeignKeyField(Categories.id)]): List of
                every Categories which contains the current product.
            :self.description (p.TextField()): Descriptionof the product. Can be empty
            :self.nutriscore (p.CharField(1)): The French nutrition grade. Must be
                in between 'A' and 'E'.
            :self.url (p.TextField()): The URL to the OpenFoodFacts product page.
            :self.stores (list[ForeignKeyField(Stores.id)]): The list of the stores
                where the user can buy the selected product.
            :self.fk_product (ForeignKeyField(Product.name))
            Methods :
            ---------
        """