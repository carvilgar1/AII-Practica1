#encoding:utf-8
from main.models import Rating, Libro, Idiomas
import csv

path = "goodreads-dataset"

def deleteTables():
    Idiomas.objects.all().delete()
    Libro.objects.all().delete()
    Rating.objects.all().delete()


def populateIdioma():
    print("Loading idiomas...")
    
    lista=set()
    fileobj=open(path+"\\bookfeatures.csv", "r", encoding="utf-8")
    next(fileobj)
    for line in csv.reader(fileobj, delimiter=";"):
        lista.add(Idiomas(idioma=str(line[4].strip())))
    fileobj.close()
    Idiomas.objects.bulk_create(lista)
    
    print("Idiomas inserted: " + str(Idiomas.objects.count()))
    print("---------------------------------------------------------")  

def populateLibro():
    print("Loading libros...")
    
    lista=[]
    fileobj=open(path+"\\bookfeatures.csv", "r", encoding="utf-8")
    next(fileobj)
    for line in csv.reader(fileobj, delimiter=";"):
        lista.append(Libro(idLibro=int(line[0].strip()), titulo=str(line[1].strip()), autor=str(line[2].strip()), genero=str(line[3].strip()), idioma=Idiomas.objects.get(idioma=str(line[4].strip()))))
    fileobj.close()
    Libro.objects.bulk_create(lista)
    
    print("Libros inserted: " + str(Libro.objects.count()))
    print("---------------------------------------------------------")  
    
def populateRating():
    print("Loading puntuaciones...")
        
    lista=[]
    fileobj=open(path+"\\ratings.csv", "r")
    next(fileobj)
    for line in csv.reader(fileobj, delimiter=";"):
        lista.append(Rating(rating=str(line[0].strip()), userId=int(line[1].strip()), libro=Libro.objects.get(pk=int(line[2].strip()))))
    fileobj.close()
    Rating.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    print("Ratings inserted: " + str(Rating.objects.count()))
    print("---------------------------------------------------------")


    
    
def populateDatabase():
    deleteTables()
    populateIdioma()
    populateLibro()
    populateRating()
    print("Finished database population")

