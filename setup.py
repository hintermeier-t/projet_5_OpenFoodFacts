""" The ``Setup`` Script.

Is used to create the database from scratch, and reset the database.

"""


import config as c

creator = c.Configuration()
creator.create()