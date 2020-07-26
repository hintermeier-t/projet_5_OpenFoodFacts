# projet_5_OpenFoodFacts
Open Classrooms Python Project n°5 : utilisez les données d'Open Food Facts
Version 1.5 07/25/2020

------------------------
GENERAL INFORMATIONS
------------------------
This project DO NOT contain any executable file.
Python 3.8, pip and pipenv are required to run the program.
You can get python at : https://www.python.org/downloads/
            pip at : https://pip.pypa.io/en/stable/installing/
            pipenv installation instruction at : https://pypi.org/project/pipenv/
            
Also, you will need MySQL 8.0 (or greater) and you may need mysql-connector-python :
You can grab them here :    https://dev.mysql.com/downloads/
                            https://dev.mysql.com/doc/connector-python/en/ 
------------------------
INSTALLATION / LAUNCHING THE PROGRAM
------------------------
In a command prompt do:
>pipenv install
The environnement should loads itself. Then do :
>pipenv run python -m main install
This should create the database and download the data.
Installing should last around 5 minutes.
At last, when installed, just run :
>pipenv run python -m main
And you will be directlycdirected to the Starting menu
WARNING : "python3" may in some cases be used instead of "python".

------------------------
KNOWN ISSUES (On Windows)
------------------------
- I've got a "raise ImproperlyConfigured('MySQL driver not installed!')" WARNING
    Make sure Windows let MySQL starts atomatically on your computer
    (Use the MySQL installer to enable it)

========================
AUTHOR
========================
Name : Thomas Hintermeier
Contact : hintermeier-t@protonmail.com
