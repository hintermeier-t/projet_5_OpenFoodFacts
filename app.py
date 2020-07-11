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
        self.menu = {
            "1": "Accueil",
            "2": "Categories",
            "3": "Favoris",
            "4": "Quitter"
        }

    def choice(self, **args):
        """
            The choice method verify the user's input.
        """
        print("Voici le menu:")
        for key, value in self.menu.items():
            print(key, ' : ', value)
        rep = ""
        while rep.startswith("__") or rep not in self.menu.keys() or rep == "":
            rep = input("Où désirez-vous aller ?: ")
        return self.menu[rep].lower(), args
 
    def enregistrement(self, cat, **args):# limiter
        """
            The enregistrement sub-menu links a product to its substitutes.
        """

        produits = data.DataSubstitution(cat)
        cat_ch = produits.display()
        if cat_ch != 'p':
            produits.select(int(cat_ch))
            save = produits.substitution(int(cat_ch))
        return self.choice()
       

    def accueil(self, **args):
        """
            The starting menu.
        """

        print("Bienvenue dans le programme de Recherche d'Aliments Saint")
        return self.choice()
        

    def categories(self, **args):
        """
            The categories method prints and ask the user to pick a category
            among 5 randomly chose.
        
        """

        print("Voici quelques catégories parmis lesquelles choisir:")
        selection = data.DataCategories()
        selection.display()
        choix = selection.select()
        if choix != 'p':
            self.enregistrement(int(choix))
        return self.choice()

    def favoris(self, **args):
        """
            The favoris menu prints the Substitutes table.
        """

        substitution_table = data.DataFavorites()
        return self.choice()

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
