# coding: utf-8

""" The Configuration module
    ========================

    This Module will store the username and the password to access Databse in
    `tables.py` file.
"""

import getpass


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

        self._user = input("Entrez votre User MySQL: ")
        self._password = getpass.getpass("Entrez votre mot de passe MySQL: ")
        self._host = "127.0.0.1"

    @property
    def user(self):
        return self._user

    @property
    def password(self):
        return self._password

    @property
    def host(self):
        return self._host