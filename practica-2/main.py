# encoding: utf-8
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request
import re
import os 
import ssl
from datetime import datetime
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser

#Error SSL
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

#Esta función crea el esquema donde se almacenaran los documentos
def crea_schema():
    return Schema(field_1 = TEXT(stored=TRUE), 
                field_2 = TEXT(stored=TRUE), 
                field_3 = TEXT(stored=TRUE),
                field_n = KEYWORD(stored = True, commas=True, lowercase=True),
                url = ID(stored = True))


def crea_index(dirindex):
    """
    Esta funcion crea un nuevo directorio en la carpeta de ejecucion del programa para almacenar el indice.
    Tambien crea un nuevo indice si el directorio esta vacio. 
    
    Parametros:
        -dirindex -> String: Nombre de la carpeta que contendra el indice
    """
    if not os.path.exists(dirindex):
            os.mkdir(dirindex)

    if not len(os.listdir(dirindex))==0:

        sn=messagebox.askyesno(message="Desea reindexar?(s/n)", title="Indice no vacío")
    else:
        sn=True 
    if sn == True:
        ix = create_in(dirindex, schema=crea_schema())
        writer = ix.writer()
        #Aqui se hace el scraping y se va anyadiendo individualmente cada documento con writer.add_document...               
        writer.commit()

def ejemplo_busqueda():
    ix=open_dir('indice')   

    with ix.searcher() as searcher:
        myquery = MultifieldParser(["asunto","contenido"], ix.schema).parse('query')
        results = searcher.search(myquery)

def buscar_titulo():
    '''muestre  una  ventana  con un entry que permita al  
    usuario  introducir varias palabras, y muestre  en  otra ventana  (con una  
    listbox    con    scrollbar)  todas  las  noticias  (categoría,  fecha,  título)  que 
    contengan alguna de esas palabras en el título.'''
    #TODO

def buscar_resumen_titulo():
    #TODO
    '''muestre  una  ventana  con un entry que 
    permita al  usuario  introducir una frase, y muestre  en  otra ventana  (con una  
    listbox  con  scrollbar) todas las noticias (categoría, fecha, título, resumen) 
    que contengan esa frase en el resumen o el título. '''

def buscar_fecha():
    #TODO
    '''muestre  una  ventana  con un entry que  permita  al  
    usuario  introducir una fecha (en formato dd MMM aaaa, por ejemplo ’11 
    nov 2021’), y  muestre  en  otra ventana (con una  listbox  con  scrollbar)  
    todas las noticias (categoría, fecha, título) desde ese día (inclusive)'''
    

def buscar_categoria():
    #TODO
    '''muestre   una    spinbox  que  permita  al    usuario  
    seleccionar una categoría de todas las que hay en el índice, y muestre  en  otra 
    ventana  (con una  listbox  con  scrollbar) todas las noticias (categoría, fecha, 
    título) de dicha categoría.'''

def eliminar_noticia():
    #TODO
    '''muestre una ventana con un botón y un entry que 
    permita al usuario introducir un título de noticias (o palabras que estén en el título).  
    Cuando se pulse el botón, se muestra una lista con las noticias (categoría, fecha, 
    título) con dicho título. A continuación se muestra una ventana para que el usuario 
    confirme que desea realizar los cambios. Si se confirma, se eliminan dichas noticias'''

if __name__ == '__main__':
    #Este codigo permite generar una ventana raiz con un menu
    root = Tk()
    menu = Menu(root)
    fila1 = Menu(menu, tearoff=0)
    fila1.add_command(label='Cargar', command=lambda: crea_index('indice'))
    fila1.add_command(label="Salir", command=root.destroy)

    opcion_datos = menu.add_cascade(label='Datos', menu = fila1)

    fila2 = Menu(menu, tearoff=0)
    fila2.add_command(label='Título', command=buscar_titulo)
    fila2.add_command(label="Resumen o Título", command=buscar_resumen_titulo)
    fila2.add_command(label="Fecha", command=buscar_fecha)
    fila2.add_command(label="Categoría", command=buscar_categoria)

    opcion_buscar = menu.add_cascade(label='Buscar', menu = fila2)

    menu.add_command(label='Eliminar Noticias', command=eliminar_noticia)

    root.configure(menu=menu)
    root.mainloop()