import app
import tables
import sys
import install

import sys

import getpass #  Will be used to enter the user password when accessing / creating Database

import tables.py

def main ():


db = tables.db

db.close() #- if not closed properly on precedent use

if "install" in sys.argv: 
    
    db.connect()
    raw_data = install.Data()
    db.create_tables([tables.Products, tables.Categories, tables.Stores, tables.Categorized, tables.Buyable, tables.Substitutes])
    clean_data = install.Cleaner(raw_data.data)
    save = install.Saver(clean_data.cleaned_data)
    db.close()

db.connect()
appli = app.Application(tables.Categories)
appli.start()
db.close()

