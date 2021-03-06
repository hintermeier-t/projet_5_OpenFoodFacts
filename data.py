"""
    THE ``data`` MODULE
    =====================

    Will be used to query the database, and send the informations to the user.

    The Classes :
    -------------

    *DataCategories : Will select 5 random categories and permit to select
        one.
    *DataSubstitution : This class links the categories to the products. it is
        designed to select a product in a given category, and select all the
        related products with better nutriscore.
    *DataFavorites : Used to select and display every saved row of the
        Substitutes table. (In fact displays the products informations).
"""

# Pypi module
from peewee import fn

# Custom module
import tables as tables


class DataCategories:
    """
    The Data_categories class selects 5 random rows from the Categories
    table and allows the user to select one.

    Attributes :
    ------------

    :self.data (query): Contains the 5 random rows
    Methods :
    ---------
    :__init__ (self): just send the query stores in self.data.
    :display(self): print every selected category (its ID and its Name).
    :select(self): Ask the use to chose one of the 5 categories, or pass
        the choice.
    """

    def __init__(self):
        """
            The __init__ method send the query and save it in self.data

            SQL :
                SELECT * FROM Categories
                ORDER BY RAND ()
                LIMIT 5;
        """

        self.data = tables.Categories.select().order_by(fn.Rand()).limit(5)

    def display(self):
        """
            The display method just prints the 5 categories
        """

        for cat in self.data:
            print("ID :", cat.id, " Nom : ", cat.name)

    def select(self):
        """
            The select method ask the user to chose one of the 5 categories
        """
        reponse = ""
        while reponse != 'p' and reponse not in self.data:
            reponse = input(
                "Choisissez une des catégories en entrant son ID (ou"
                "  entrez \"p\" pour revenir à l'affichage du menu: "
            )
            return reponse


class DataSubstitution:

    """
        The Data_substitution class links the selected category with the
        products it contains, and ask the user to chose a product
        before searching for one or several healthier products to save.

        Attributes :
        ------------

        :self.prod (query): Contains every product linked to the category.
        :self.final_query (query):  Contains the healthier products.

        Methods :
        ---------
        :__init__ (self): just send the query stores in self.prod.
        :display(self, product_id): print every selected  product, and ask to
            select one.
        :select(self, product_id): Searches for all healthier products. If
            there is at least one, displays it on screen.
        :substitution(self, product_id): Save a new row in the Substitutes
            table with the original product and the healthier one.
    """

    def __init__(self, cat_id):
        """
            The __init__ method. Send the query and save it into self.prod.

            SQL query :
                    SELECT * FROM Products
                    JOIN Categorized
                    WHERE (Products.id = Categorized.fk_product_id
                        AND Categorized.fk_category_id = cat_id);

            Args:
            ----------
            :cat_id (int): the ID of a category in the Categories table.
        """
        self.prod = (
            tables.Products.select()
            .join(tables.Categorized)
            .where(
                (tables.Products.id == tables.Categorized.fk_product)
                & (tables.Categorized.fk_category == cat_id)
            )
        )

    def display(self):
        """
            The display method just prints the products related to the
            'cat_id' category.

            Returns :
            ---------
            An input (int). The chosen product to substitutes.

        """
        for produit in self.prod:
            print("\n",
                  "ID: ",
                  produit.id,
                  "\tNOM: ",
                  produit.name,
                  "\tMARQUE: ",
                  produit.brand_name,
                  "\tNUTRISCORE: ",
                  produit.nutriscore
                  )
        choix = input(
            "Sélectionner l'ID d'un produit pour trouver un substitut ou\
             \"p\" pour retourner au menu précédent: "
        )
        return choix

    def select(self, product_id):
        """
            The Select method looks for all the substitution products.
            And displays the best results.

            Arg:
            ---------
            :product_id (int): the ID of the product to substitute. The
                complete row is saved in 'ref'.

            SQL:
            SELECT * FROM Products
            WHERE Products.id IN (
                SELECT fk_product_id FROM Categorized
                WHERE (Categorized.fk_category_id
                 IN ( SELECT fk_category_id FROM Categorized
                    WHERE Categorized.fk_product_id = product_id)
                )
                    AND Categorized.fk_product_id != product_id
                    AND Products.nutriscore IN ref_ns
            );

        """
        ref = tables.Products.get(tables.Products.id == product_id)
        ref_ns = ['A', 'B', 'C', 'D', 'E']
        ref_ns = ref_ns[: ref_ns.index(str(ref.nutriscore))]
        prod_cat = set()
        prod_comp = set()

        for element in tables.Categorized.select().where(
            tables.Categorized.fk_product == product_id
        ):
            prod_cat.add(element.fk_category)
        
        for element in (tables.Categorized.select(
                    tables.Categorized.fk_product,
                    fn.count(tables.Categorized.fk_category).alias('nb'))
                    .where(tables.Categorized.fk_category.in_(prod_cat))
                    .group_by(tables.Categorized.fk_product)
                    .order_by(fn.count(tables.Categorized.fk_category).desc())
                    ):
            prod_comp.add(element.fk_product)
            
        
        self.final_query = tables.Products.select().where(
            tables.Products.id.in_(prod_comp)
            & tables.Products.nutriscore.in_(ref_ns)
        ).limit(5)

        if self.final_query.exists():
            for produit in self.final_query:
                print(
                    "ID: ",
                    produit.id,
                    "\nNOM: ",
                    produit.name,
                    "\nMARQUE: ",
                    produit.brand_name,
                    "\nNUTRISCORE: ",
                    produit.nutriscore,
                    "\nURL OPENFOODFACTS: ",
                    produit.url,
                    "\n",
                )
                for magasin in (tables.Stores.select()
                                .join(tables.Buyable)
                                .where(tables.Buyable.fk_product == produit.id)
                                .group_by(tables.Stores.name)):
                                print (magasin.name)

        else :
            print("Désolé, nous n'avons trouvé aucune alternative à votre produit")

    def substitution(self, product_id):
        """
            The substitution  method store the selected substitute and its
            original product in the Substitutes table.

            SQL:
            REPLACE INTO Substitutes
                (fk_base_product_id, fk_healthier_product_id)
            VALUES (product_id, reponse);

        """
        reponse = ""
        while reponse != 'p' and reponse not in self.final_query:
            reponse = input(
                "Choisissez un des produits à substituer en entrant son ID ou"
                "  entrez \"p\" pour revenir à l'affichage du menu: "
            )
            if reponse != 'p':
                tables.Substitutes.get_or_create(
                    fk_base_product=tables.Products.get(
                        tables.Products.id == product_id
                    ),
                    fk_healthier_product=tables.Products.get(
                        tables.Products.id == reponse
                    )
                )
            print("Produit enregistré")
        return reponse


class DataFavorites:

    """
        The Data_favorites class will query the database to select every
        product peer set as foreign key in the Substitutes table:
        original_product/healthier_product.

        Attribute:
        -----------
        :self.substitutes (query): Selects all the Substitutes class to
            work on.

        Method:
        -------
        :__init__(self): Selects and display the products.
    """

    def __init__(self):
        """
            The __init__ method. Selects and display the products from the
            Substitutes table.

            First, it queries the Substitutes table to get all the rows. Then,
            it queries every product related to the foreign keys and displays
            it.
        """

        self.substitutes = tables.Substitutes.select()
        print("Voici les produits que vous avez enregistré:\n\n")
        for product in self.substitutes:
            original = tables.Products.get(
                tables.Products.id == product.fk_base_product
            )
            healthier = tables.Products.get(
                tables.Products.id == product.fk_healthier_product
            )
            print(
                "Produit de base :",
                "Produit de substitution :".rjust(
                    100-len("Produit de base :")),
                "\nID:",
                original.id,
                "ID:".rjust(100-len(str(original.id))),
                healthier.id,
                "\nNom:",
                original.name,
                "Nom:".rjust(100-len(str(original.name))),
                healthier.name,
                "\nMarque:",
                original.brand_name,
                "Marque:".rjust(100-len(str(original.brand_name))),
                healthier.brand_name,
                "\nNutriscore:",
                original.nutriscore,
                "Nutriscore:".rjust(100-len(str(original.nutriscore))),
                healthier.nutriscore,
                "\nURL OPENFOODFACTS: ",
                    original.url,
                "URL OPENFOODFACTS: ".rjust(100-len(str(original.nutriscore))),
                    healthier.url,
                "\n\n",
            )
