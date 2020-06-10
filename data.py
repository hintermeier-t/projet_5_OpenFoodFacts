import random
import tables


class Data_categories:
    def __init__(self, Categories):
        self.data = dict()
        for categorie in Categories.select():
            self.data.update({Categories.id:Categories.name})
    
    def display (self):
        for cat in self.data :
            print(cat)
    
    def select (self, n:int):
        r = random.sample(list(self.data.keys()), n)
        for num in r:
            selection.update({num,self.data.et(num)})
        return selection