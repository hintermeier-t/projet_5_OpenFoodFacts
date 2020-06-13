import peewee
from peewee import fn
import random
import tables


class Data_categories:
    def __init__(self):
        print(tables.Categories.select().order_by(fn.Rand()).limit(5))
    
    def display (self):
        for cat in self.data :
            print(cat)
    
    def select (self, n:int):
        r = random.sample(list(self.data.keys()), n)
        for num in r:
            selection.update({num,self.data.et(num)})
        return selection