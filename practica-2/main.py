# encoding: utf-8
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib.request
import re
import os 
import ssl
from whoosh.index import create_in,open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD
from whoosh.qparser import QueryParser, MultifieldParser
from whoosh import qparser
import datetime
import locale
#Error SSL
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

locale.setlocale(locale.LC_TIME, "es_ES")

url = 'https://www.sensacine.com/'

#Esta función crea el esquema donde se almacenaran los documentos
def crea_schema():
    return Schema(categoria = TEXT(stored=TRUE), 
                fecha = DATETIME(stored=TRUE), 
                titulo = TEXT(stored=TRUE),
                resumen = TEXT(stored = True))


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
        j=0
        for i in range (1,3):
            f = urllib.request.urlopen(url+'noticias/?page=' +str(i))
            bs = BeautifulSoup(f,'lxml')
            for pelicula in bs.find("div", class_="gd-col-left").find_all('div', class_="meta"):
                j=j+1
                
               
                title = pelicula.find("a", class_="meta-title-link").text
                date = pelicula.find("div",class_="meta-date").text.split(",")
                parsed_date  = datetime.datetime.strptime(date[1].strip(), "%d de %B de %Y")
                category = pelicula.find("div",class_="meta-category").text[11:].strip()
                content = ''
                if not pelicula.find("div", class_="meta-body") == None:
                    content = pelicula.find("div", class_="meta-body").text

                writer.add_document(categoria = str(category), fecha = parsed_date, titulo = str(title), resumen = str(content))
        messagebox.showinfo("Fin  de indexado", "Se han indexado " + str(j) + " noticias de peliculas.")
        writer.commit()

def ejemplo_busqueda():
    ix=open_dir('indice')   

    with ix.searcher() as searcher:
        myquery = MultifieldParser(["asunto","contenido"], ix.schema).parse('query')
        results = searcher.search(myquery)

if __name__ == '__main__':
    crea_index('indice')