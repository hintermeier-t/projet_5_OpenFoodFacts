# coding: utf-8

""" The Configuration module
    ========================

    This Module will store the username and the password to access Databse in
    `tables.py` file.
"""

import getpass
import os

import dotenv
import mysql.connector as m


class Configuration:
    """
        The Configuration class gather the required informations to connect to the 
        database.

        Attributes:
        -----------
        :self._user (str): The MySQL username.
        :self._password (getpass): The MYSQL user's password.
        :self._host (str): Where to connect the database.
    """

    def __init__(self):
        """
            The __init__ method ask the user and the password to connect the
            MySQL Database on localhost.
        """

        dotenv.load_dotenv()
        if os.getenv("P_USER") == "":
            self._user = input("Entrez votre User MySQL: ")
        else:
            self._user = os.getenv("P_USER")
        if os.getenv("P_PASSWD") =="":
            self._password = getpass.getpass("Entrez votre mot de passe MySQL: ")
        else:
            self._password = os.getenv("P_PASSWD")
        self._host = os.getenv("P_HOST")

    def create (self):
        creation = m.connect(
            host = self._host,
            user = self._user,
            password = self._password
        )
        cursor = creation.cursor()
        cursor.execute("DROP DATABASE IF EXISTS openfoodfacts")
        cursor.execute("CREATE DATABASE IF NOT EXISTS openfoodfacts")
        creation.close()
        
    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def host(self):
        return self._host