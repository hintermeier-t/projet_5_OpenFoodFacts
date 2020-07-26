# coding: utf-8
"""
    The main module, starting the program.

"""
# - Importing Standard Modules:
import sys
import getpass

# - Importing Custom Modules:
import app
import tables
import install
import config


def main():
    """
        Main function

    """
    db = tables.db
    db.close()  # - if not closed properly on precedent use
    
    
    if "install" in sys.argv:
        raw_data = install.Data()
        db.create_tables([tables.Products, tables.Categories, tables.Stores,
                          tables.Categorized, tables.Buyable, tables.Substitutes])
        clean_data = install.Cleaner(raw_data.data)
        save = install.Saver(clean_data.cleaned_data)
        save.associate(clean_data.cleaned_data)
        db.close()

    db.connect()
    appli = app.Application()
    appli.start()
    db.close()


if __name__=="__main__":
    main()
