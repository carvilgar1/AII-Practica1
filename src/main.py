# encoding: utf-8
# -*- coding: utf-8 -*-

from sqlite3.dbapi2 import Cursor
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
                if('class' in children.attrs):
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

def cargar_datos():
    crear_tablas()
    instanciar_db()
    #Generar una ventana emergente de aviso
    messagebox.showinfo('Aviso', 'Los datos se han cargado correctamente')

def listar_libros():
    #Este codigo permite generar una ventana emergente que incluye una lista de elementos y un scrollbar a la derecha
    ''' muestre en una ventana (con una listbox con scrollbar) todos los (título,
    autor, editorial y precio). '''
    cursor = con.cursor()
    listado = cursor.execute('SELECT TITULO, AUTOR, EDITORIAL, PRECIO FROM LIBROS').fetchall()
    window = Toplevel()
    window.geometry('720x360')
    scroll = Scrollbar(window)
    scroll.pack(side=RIGHT, fill=Y)
    listado = Listbox(window, yscrollcommand=scroll.set)
    listado.insert(END, *listado)
    listado.pack(fill=BOTH, expand=YES)
    scroll.config(command=listado.yview)

def listar_librerias():
    #Este codigo permite generar una ventana emergente que incluye una lista de elementos y un scrollbar a la derecha
    '''muestre en una ventana (con una listbox con scrollbar) los nombres
    y teléfonos de todas las librerías que hay en la BD. '''
    cursor = con.cursor()
    listado = set(cursor.execute('SELECT LIBRERIA, TELEFONO FROM LIBROS').fetchall())
    window = Toplevel()
    window.geometry('720x360')
    scroll = Scrollbar(window)
    scroll.pack(side=RIGHT, fill=Y)
    listado = Listbox(window, yscrollcommand=scroll.set)
    listado.insert(END, *listado)
    listado.pack(fill=BOTH, expand=YES)
    scroll.config(command=listado.yview)

def libros_por_editorial():
    def search_libros(event):
        #Este codigo permite generar una ventana emergente que incluye una lista de elementos y un scrollbar a la derecha
        '''muestre en otra ventana (con una
        listbox con scrollbar) todos los libros (título, autor, estado de conservación, librería y precio) que
        hay en la BD que de esa editorial'''
        editorial = entry.get()
        cursor = con.cursor()
        listado = cursor.execute('SELECT TITULO, AUTOR, ESTADO, LIBRERIA, PRECIO FROM LIBROS WHERE EDITORIAL = ?', [editorial]).fetchall()
        window = Toplevel()
        window.geometry('720x360')
        scroll = Scrollbar(window)
        scroll.pack(side=RIGHT, fill=Y)
        listado = Listbox(window, yscrollcommand=scroll.set)
        listado.insert(END, *listado)
        listado.pack(fill=BOTH, expand=YES)
        scroll.config(command=listado.yview)
    
    #Este código permite generar una ventana con un spin box
    v = Toplevel()
    entry = Spinbox(v, values=list(editoriales)) 
    entry.bind('<Return>', search_libros)
    entry.pack()

def libros_por_titulo_o_autor():
    def search_libros(event):
        #Este codigo permite generar una ventana emergente que incluye una lista de elementos y un scrollbar a la derecha
        '''muestre en otra ventana (en una listbox con
        scrollbar) todos los libros que contengan esa palabra en el título o el autor (título, autor, estado de
        conservación, librería y precio)'''
        titulo_o_autor = entry.get()
        cursor = con.cursor()
        listado = cursor.execute('SELECT TITULO, AUTOR, ESTADO, LIBRERIA, PRECIO FROM LIBROS WHERE AUTOR = ? OR TITULO = ?', [titulo_o_autor, titulo_o_autor]).fetchall()
        window = Toplevel()
        window.geometry('720x360')
        scroll = Scrollbar(window)
        scroll.pack(side=RIGHT, fill=Y)
        listado = Listbox(window, yscrollcommand=scroll.set)
        listado.insert(END, *listado)
        listado.pack(fill=BOTH, expand=YES)
        scroll.config(command=listado.yview)
    
    #Este codigo permite generar una ventana emergente con un entry y un label se envi­a al hacer Enter sobre entry
    window1 = Toplevel()
    label = Label(window1, text='Introduce el titulo o autor')
    label.pack()
    entry = Entry(window1)
    entry.pack()
    entry.bind('<Return>', search_libros)
    window1.mainloop()

if __name__ == '__main__':
    #Este codigo permite generar una ventana rai­z con un menu
    
    root = Tk()
    menu = Menu(root)
    fila1 = Menu(menu, tearoff=0)
    fila1.add_command(label='Cargar', command=cargar_datos)
    fila1.add_command(label='Salir', command=root.destroy)

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
