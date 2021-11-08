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

if __name__ == '__main__':
    crea_index('indice')