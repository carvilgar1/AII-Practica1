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

def buscar_titulo():
    '''muestre  una  ventana  con un entry que permita al  
    usuario  introducir varias palabras, y muestre  en  otra ventana  (con una  
    listbox    con    scrollbar)  todas  las  noticias  (categoría,  fecha,  título)  que 
    contengan alguna de esas palabras en el título.'''
    def search(event):
        ix=open_dir('indice')   

        with ix.searcher() as searcher:
            myquery = QueryParser('titulo', ix.schema).parse(entry.get())
            results = searcher.search(myquery)
            #Este codigo permite generar una ventana emergente que incluye una lista de elementos y un scrollbar a la derecha
            window = Toplevel()
            window.geometry('720x360')
            scroll = Scrollbar(window)
            scroll.pack(side=RIGHT, fill=Y)
            listado = Listbox(window, yscrollcommand=scroll.set)
            for r in results:
                listado.insert(END, r['categoria'])
                listado.insert(END, r['fecha'])
                listado.insert(END, r['titulo'])
                listado.insert(END, '')
            listado.pack(fill=BOTH, expand=YES)
            scroll.config(command=listado.yview)
    
    #Este codigo permite generar una ventana emergente con un entry y un label se envÃ­a al hacer Enter sobre entry
    window1 = Toplevel()
    label = Label(window1, text='Inserte palabras para buscar en el título')
    label.pack()
    entry = Entry(window1)
    entry.pack()
    entry.bind('<Return>', search)
    window1.mainloop()

def buscar_resumen_titulo():
    '''muestre  una  ventana  con un entry que 
    permita al  usuario  introducir una frase, y muestre  en  otra ventana  (con una  
    listbox  con  scrollbar) todas las noticias (categoría, fecha, título, resumen) 
    que contengan esa frase en el resumen o el título. '''
    def search(event):
        ix=open_dir('indice')   

        with ix.searcher() as searcher:
            myquery = MultifieldParser(["titulo","resumen"], ix.schema).parse(entry.get())
            results = searcher.search(myquery)
            #Este codigo permite generar una ventana emergente que incluye una lista de elementos y un scrollbar a la derecha
            window = Toplevel()
            window.geometry('720x360')
            scroll = Scrollbar(window)
            scroll.pack(side=RIGHT, fill=Y)
            listado = Listbox(window, yscrollcommand=scroll.set)
            for r in results:
                listado.insert(END, r['categoria'])
                listado.insert(END, r['fecha'])
                listado.insert(END, r['titulo'])
                listado.insert(END, r['resumen'])
                listado.insert(END, '')
            listado.pack(fill=BOTH, expand=YES)
            scroll.config(command=listado.yview)
    
    #Este codigo permite generar una ventana emergente con un entry y un label se envÃ­a al hacer Enter sobre entry
    window1 = Toplevel()
    label = Label(window1, text='Inserte palabras para buscar en el título o en el resumen')
    label.pack()
    entry = Entry(window1)
    entry.pack()
    entry.bind('<Return>', search)
    window1.mainloop()


def buscar_fecha():
    '''muestre  una  ventana  con un entry que  permita  al  
    usuario  introducir una fecha (en formato dd MMM aaaa, por ejemplo ’11 
    nov 2021’), y  muestre  en  otra ventana (con una  listbox  con  scrollbar)  
    todas las noticias (categoría, fecha, título) desde ese día (inclusive)'''

    def search(event):
        fecha = entry.get().strip()
        if re.match(r'\d{2} [a-z]{3} \d{4}', fecha):
            ix=open_dir('indice')   

            with ix.searcher() as searcher:
                myquery = MultifieldParser(["titulo","resumen"], ix.schema).parse(fecha)
                results = searcher.search(myquery)
                #Este codigo permite generar una ventana emergente que incluye una lista de elementos y un scrollbar a la derecha
                window = Toplevel()
                window.geometry('720x360')
                scroll = Scrollbar(window)
                scroll.pack(side=RIGHT, fill=Y)
                listado = Listbox(window, yscrollcommand=scroll.set)
                for r in results:
                    listado.insert(END, r['categoria'])
                    listado.insert(END, r['fecha'])
                    listado.insert(END, r['titulo'])
                    listado.insert(END, '')
                listado.pack(fill=BOTH, expand=YES)
                scroll.config(command=listado.yview)
        else:
            #Generar una ventana emergente de aviso
            messagebox.showinfo('Error', 'Formato de fecha incorrecto')

    #Este codigo permite generar una ventana emergente con un entry y un label se envia al hacer Enter sobre entry
    window1 = Toplevel()
    label = Label(window1, text='Introducir una fecha (en formato dd MMM aaaa)')
    label.pack()
    entry = Entry(window1)
    entry.pack()
    entry.bind('<Return>', search)
    window1.mainloop()
    

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