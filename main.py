import sys
import os

import getpass #  Will be used to enter the user password when accessing / creating Databasepy


if 'install' in str(sys.argv):
    #Call installation script the minimum required informations. 
    print("Hello World")



password = getpass.getpass("Enter password :")
if password == '2skys':
     print("""Well Done !""")