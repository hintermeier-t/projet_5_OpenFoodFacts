import peewee
from peewee import fn
import random
import tables as tables


class Data_categories:
    def __init__(self):
        self.data = tables.Categories.select().order_by(fn.Rand()).limit(5)
    
    def display (self):
        for cat in self.data :
            print("ID :", cat.id, " Nom : ", cat.name)
    
    def select (self):
        reponse = ""
        while reponse != 'p' and reponse not in self.data:
            reponse = input("Choisissez une des catégories en entrant son ID (ou"\
            "  entrez \"p\" pour revenir à l'affichage du menu: ")
            if reponse == 'p' :
                return 0
            else:
                return reponse
        return None

class Data_substitution :
    def __init__(self, cat_id):
        self.prod =\
            tables.Products.select()\
                .join(tables.Categorized)\
                .where((tables.Products.id == tables.Categorized.fk_product)\
                    & (tables.Categorized.fk_category == cat_id))
    
    def display(self):
        for produit in self.prod:
            print("ID: ", produit.id, "\nNOM: ", produit.name, "\nMARQUE: ", produit.brand_name, "\nNUTRISCORE: ", produit.nutriscore, "\n\n\n")
            return input("Veuillez sélectionner l'ID d'un produit pour trouver un substitut")
        
    def select(self, product_id):
        ref = tables.Products.get(tables.Products.id == product_id)
        ref_ns = ['A','B','C','D','E']
        ref_ns = ref_ns[:ref_ns.index(str(ref.nutriscore))]
        prod_cat = []
        prod_comp = []
               
        for element in tables.Categorized.select()\
            .where(tables.Categorized.fk_product == product_id):
                prod_cat.append(element.fk_category)

        for element in tables.Categorized.select()\
            .where(tables.Categorized.fk_category.in_(prod_cat)\
                & tables.Categorized.fk_product != product_id):
            prod_comp.append(element.fk_product)

        self.final_query = tables.Products.select()\
            .where(tables.Products.id.in_(prod_comp) &\
            tables.Products.nutriscore.in_(ref_ns))

        if self.final_query.exists():
            for produit in self.final_query:
                print("ID: ", produit.id, "\nNOM: ", produit.name, "\nMARQUE: ", produit.brand_name, "\nNUTRISCORE: ", produit.nutriscore, "\n\n\n")
    def substitution (self, product_id):

        reponse = ""
        while reponse != 'p' and reponse not in self.final_query:
                reponse = input("Choisissez un des produits à substituer en entrant son ID (ou"\
                "  entrez \"p\" pour revenir à l'affichage du menu: ")
                if reponse == 'p' :
                    break
                else:
                    tables.Substitutes.get_or_create(
                        fk_base_product = tables.Products.get\
                            (tables.Products.id == product_id),
                        fk_healthier_product = tables.Products.get\
                            (tables.Products.id == reponse)
                    )
                    print("Produit enregistré")
             


            #1 : Sélectionne depuis CATEGORIZED toutes les (id) catégories auxqelles appartient le produit donné (product_id) -> liste

            #2: Sélectionne depuis CATEGORIZED tous les (id) produits dont la catégorie associée est dans (liste) -> liste2

            #3: Sélectionne depuis PRODUITS tous les (id, nom, marque description nutriscore) produits dont l'id est dans (liste2) ET dont le nutriscore est meilleur que le produit (id_product)

    