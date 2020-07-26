# coding: utf-8
""" 
    Setup script. Create the database
"""

import mysql.connector as m
import dotenv

import getpass
import os

dotenv.load_dotenv()
if os.getenv("P_USER") == "":
    user = input("Entrez votre User MySQL: ")
else:
    user = os.getenv("P_USER")
if os.getenv("P_PASSWD") =="":
    password = getpass.getpass("Entrez votre mot de passe MySQL: ")
else:
    password = os.getenv("P_PASSWD")
host = os.getenv("P_HOST")

creation = m.connect(host = host, user = user, password = password)
cursor = creation.cursor()
cursor.execute("CREATE DATABASE openfoodfacts")
creation.close()