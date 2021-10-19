# encoding: utf-8
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import sqlite3
import urllib.request
import re
import os, ssl

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

def cargar_datos():
    crear_tablas()
    instanciar_db()

def listar_libros():
    None

def listar_librerias():
    None

def libros_por_editorial():
    None

def libros_por_titulo_o_autor():
    None

if __name__ == '__main__':
    #Este codigo permite generar una ventana rai­z con un menu
    root = Tk()
    menu = Menu(root)
    fila1 = Menu(menu, tearoff=0)
    fila1.add_command(label='Cargar', command=cargar_datos)
    fila1.add_command(label='Salir', command=root.quit)

    opcion_datos = menu.add_cascade(label='Datos', menu = fila1)

    fila2 = Menu(menu, tearoff=0)
    fila2.add_command(label='Libros', command=listar_libros)
    fila2.add_command(label="Librerias", command=listar_librerias)
    opcion_buscar = menu.add_cascade(label='Listar', menu = fila2)

    fila3 = Menu(menu, tearoff=0)
    fila3.add_command(label='Libros por editorial', command=libros_por_editorial)
    fila3.add_command(label="Libros por título o autor", command=libros_por_titulo_o_autor)
    opcion_buscar = menu.add_cascade(label='Buscar', menu = fila3)

    root.configure(menu=menu)
    root.mainloop()
