# encoding: utf-8
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import sqlite3
import urllib.request
import re
import os 
import ssl

#Error SSL
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

#Se define una variable estatica a la que pueda acceder cualquier funcion. Crea y se conecta a una base de datos
con = sqlite3.connect('libros.db')
url = 'https://www.uniliber.com/buscar/libros_pagina_' 
url2 = '?descripcion%5B0%5D=CL%C3%81SICOS'
editoriales = set()

#Esta funcion crea las tablas en la database.db
def crear_tablas():
    cursor = con.cursor()
    query = 'DROP TABLE IF EXISTS LIBROS'
    query1 = '''CREATE TABLE LIBROS (TITULO     TEXT    NOT NULL,
                                    AUTOR       TEXT,
                                    EDITORIAL   TEXT,
                                    ESTADO      TEXT,
                                    PRECIO      FLOAT,
                                    LIBRERIA    TEXT,
                                    TELEFONO    TEXT

                                )'''
    cursor.execute(query)
    cursor.execute(query1)
    con.commit()

#Esta funcion instancia la database.db a partir del scrapping a una pagina web
def instanciar_db():
    crear_tablas()
    cursor = con.cursor()
    for i in range(2):

        web = urllib.request.urlopen(url+str(i+1)+url2).read().decode('utf-8')
        arbol = BeautifulSoup(web, 'lxml')
        descripciones = arbol.findAll("div", class_="description")
        for descripcion in descripciones:
            titulo = descripcion.find("a", class_="title").string
            autor = descripcion.find("div", class_="subtitle").string
            editorial = ''
            estado = ''
            for children in descripcion.findAll("div"):
                if('class' in children.attrs and len(children.contents)<2):
                    continue
                print(children.strong)
                if(children.strong == "Editorial:"):
                    editorial = children.contents[2]
                    print(editorial)
                if(children.strong == "Estado de conservación:"):
                    estado = children.contents[2]
                print(editorial,estado)
            precio = descripcion.find("span", class_="precio").string.replace("€","")
            # print(titulo, autor,editorial,estado,precio)

    
    
    
    con.commit()

if __name__ == '__main__':

    raiz = Tk()
    instanciar_db()
    raiz.mainloop()
