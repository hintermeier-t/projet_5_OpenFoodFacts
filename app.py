import data


class Application:
    """
        Tthe Application class is set to manage the navigating menu, and allow
        the user to set up favorite products, look for a product etc...

        Attributes :
        ------------
        :self.next (str): the name of the next sub-menu.
        :self.menu (str): just a string used to display the commands.
        self.running (bool): Controls the execution loop.

        Methods:
        --------
        :__init__(self): Just sets the first menu to "Accueil".
        :choice(self, rep): verify the user's input.
        :enregistrement(self, cat, **args): The sub-menu which links a product
            to its substitutes.
        :accueil(self, **args): Starting menu.
        :categories(self, **args): Prints and ask the user to pick a category
            among 5 randomly chose.
        :favoris(self, **args): Prints the Substitutes table.
        :quitter(self, **args): Quit the program.
        :start(self, **args): Launch the menu, and refresh.
    """

    def __init__(self):

        """
            The __init__ method sets the first menu to "accueil".
        """

        self._next = "accueil"
        self.menu = "Voici la liste des commandes de menu :\n\
            * accueil - Menu d'Accueil\n\
            * categories - Rechercher par catégories de produits\n\
            * favoris - Afficher les produits sauvés et leurs substituts\n\
            * quitter - Quitte l'Application"

    def choice(self, rep):
        """
            The choice method verify the user's input.
        """

        if rep.startswith("__") or rep not in vars(Application)\
                or rep == "":
            return True
 
    def enregistrement(self, cat, **args):# limiter

        """
            The enregistrement sub-menu links a product to its substitutes.
        """

        produits = data.Data_substitution(cat)
        cat_ch = produits.display()
        if cat_ch == 0:
            self.reponse = "accueil"
            return self.reponse.strip(), args
        produits.select(int(cat_ch))
        save = produits.substitution(int(cat_ch))
        self.reponse = ""
        if save == 0:
            while self.choice(self.reponse):
                self.reponse = input("Où désirez-vous aller ? : ")
                if not self.reponse.startswith("__") and self.reponse in vars(Application):
                    return self.reponse.strip(), args
        self.reponse = "accueil"
        return self.reponse.strip(), args
       

    def accueil(self, **args):

        """
            The starting menu.
        """

        print("Bienvenue dans le programme de Recherche d'Aliments Saint")
        print(self.menu)
        self.reponse = ""
        while self.choice(self.reponse):
            self.reponse = input("Où désirez-vous aller ? ")
        if not self.reponse.startswith("__") and self.reponse in vars(Application):
            return self.reponse.strip(), args

    def categories(self, **args):

        """
            The categories method prints and ask the user to pick a category
            among 5 randomly chose.
        
        """

        print(self.menu)
        self.reponse = ""
        selection = data.Data_categories()
        selection.display()
        choix = selection.select()
        if choix == 0:
            while self.choice(self.reponse):
                self.reponse = input("Où désirez-vous aller ? : ")
            if not self.reponse.startswith("__") and self.reponse in vars(Application):
                return self.reponse.strip(), args
        else:
            self.enregistrement(int(choix))
        self.reponse = "accueil"
        return self.reponse, args

    def favoris(self, **args):

        """
            The favoris menu prints the Substitutes table.
        """

        substitution_table = data.Data_favorites()
        print(self.menu)
        self.reponse = input("Où désirez-vous aller ? ")
        if not self.reponse.startswith("__") and self.reponse in vars(Application):
            return self.reponse.strip(), args

    def quitter(self, **args):
        
        """
            Exit the loop and doing so, the program.
        """

        print("Fin du programme")
        self.running = False
        return "", args

    def start(self, **args):

        """
            Launch the menu, and refresh.
        """

        self.running = True
        args = {}
        while self.running:
            ret = getattr(self, self._next)(**args)
            self._next, args = ret
