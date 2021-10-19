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
                if('class' not in children.attrs and len(children.contents)>=2):
                    if(children.contents[1].text == "Editorial:"):
                        editorial = children.contents[2].strip()
                    if(children.contents[1].text == "Estado de conservación:"):
                        estado = children.contents[2].strip()
                
            precio = descripcion.find("span", class_="precio").string.replace("€","")
            link = descripcion.find("a", class_="libreria")['href']
            libreria = urllib.request.urlopen('https://www.uniliber.com' + str(link)).read().decode('utf-8')
            arbol2 = BeautifulSoup(libreria, 'lxml')
            nombre = arbol2.find("div", class_="info").find("h1").string    
            tlf = arbol2.find("div", class_="info-libreria").find("th", text="Teléfono:").findNext().text
            cursor.execute("INSERT INTO LIBROS VALUES (?,?,?,?,?,?,?);", (titulo, autor,editorial,estado,float(precio), nombre,tlf))
            print(titulo)
    count = cursor.execute("SELECT COUNT(*) FROM LIBROS").fetchone()[0]
    messagebox.showinfo("Numero de libros", "Se han almacenado " + str(count) + " libros")
    
    
    
    
    con.commit()

if __name__ == '__main__':

    instanciar_db()

