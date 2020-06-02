# coding: utf-8

""" The Configuration module
    ========================

    This Module will store the username and the password to access Databse in
    `tables.py` file.
"""
import getpass

class Configuration:
    def __init__(self):
        self._user = input("Entrez votre User MySQL: ")
        self._password = getpass.getpass("Entrez votre mot de passe MySQL: ")

    @property
    def user(self):
        return self._user
    
    @property
    def password(self):
        return self._password