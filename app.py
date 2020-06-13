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

    def accueil(self, **args):
        print("Bienvenue dans le programme de Recherche d'Aliments Saint")
        print(self.menu)
        self.reponse = ""
        while self.choice(self.reponse):
            self.reponse = input("Où désirez-vous aller ? ")
        if not self.reponse.startswith("__") and self.reponse in vars(Application):
            return self.reponse.strip(), {"key1": "value1", "key2": "value2"}

    def categories(self, **args):
        print(self.menu)
        selection = data.Data_categories()
        print(selection)
        while self.choice(self.reponse):
            self.reponse = input("Sélectionnez une catégorie ou un menu : ")
        if not self.reponse.startswith("__") and self.reponse in vars(Application):
            return self.reponse.strip(), {"key1": "value1", "key2": "value2"}
        

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