import data

class Application:

    def __init__(self, Categories):
        self._next = "accueil"
        self.menu = "Voici la liste des commandes de menu :\n\
            1. accueil - Menu d'Accueil\n\
            2. categories - Rechercher par catégories de produits\n\
            4. favoris - Afficher les produits sauvegardés et leurs substituts\n\
            5. quitter - Quitte l'Application"

    def choice(self, rep):
            if rep.startswith("__") or rep not in vars(Application)\
                or rep == "":
                return True

    def enregistrement(self, cat, **args):
        produits = data.Data_substitution(cat)
        cat_ch= produits.display()
        produits.select(int(cat_ch))
        produits.substitution(int(cat_ch))
        self.reponse=""
        while self.choice(self.reponse):
            self.reponse = input("Où désirez-vous aller ? : ")
            if not self.reponse.startswith("__") and self.reponse in vars(Application):
                return self.reponse.strip(), args         

    def accueil(self, **args):
        print("Bienvenue dans le programme de Recherche d'Aliments Saint")
        print(self.menu)
        self.reponse = ""
        while self.choice(self.reponse):
            self.reponse = input("Où désirez-vous aller ? ")
        if not self.reponse.startswith("__") and self.reponse in vars(Application):
            return self.reponse.strip(), {"key1": "", "key2": ""}

    def categories(self, **args):
        print(self.menu)
        self.reponse = ""
        selection = data.Data_categories()
        selection.display()
        choix = selection.select()
        if choix is None :
            while self.choice(self.reponse):
                self.reponse = input("Où désirez-vous aller ? : ")
            if not self.reponse.startswith("__") and self.reponse in vars(Application):
                return self.reponse.strip(), args
        else:
            self.enregistrement(int(choix))
        

    def favoris (self, **args):
        print(self.menu)
        self.reponse = input("Où désirez-vous aller ? ")
        if not self.reponse.startswith("__") and self.reponse in vars(Application):
            return self.reponse.strip(), args

    def quitter(self, **args):
        print("Fin du programme")
        self.running = False
        return "", args

    def start(self):
        self.running = True
        args = {}
        while self.running:
            self._next, args = getattr(self, self._next)(**args)