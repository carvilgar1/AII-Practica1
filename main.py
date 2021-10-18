from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import sqlite3
import urllib.request
import re

#Error SSL
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

#Se define una variable estatica a la que pueda acceder cualquier funcion. Crea y se conecta a una base de datos
con = sqlite3.connect('database.db')

#Esta funcion crea las tablas en la database.db
def crear_tablas():
    cursor = con.cursor()
    query = 'DROP TABLE IF EXISTS X'
    query1 = '''CREATE TABLE X (
                                    x   TEXT    NOT NULL,
                                    y   TEXT    NOT NULL,
                                    z   REAL    NOT NULL
                                )'''
    cursor.execute(query)
    cursor.execute(query1)
    con.commit()

#Esta funcion instancia la database.db a partir del scrapping a una pagina web
def instanciar_db():
    crear_tablas()
    cursor = con.cursor()
    web = urllib.request.urlopen('AQUI LA URL')
    arbol = BeautifulSoup(web, 'lxml')
    con.commit()

if __name__ == '__main__':
    raiz = Tk()
    raiz.mainloop()
