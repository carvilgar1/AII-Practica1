from main.models import Rating, Libro
import csv

path = "goodreads-dataset"

def deleteTables():
    pass
    #Libro.objects.all().delete()
    #Puntuacion.objects.all().delete()
  
    
def populatePuntuacion():
    print("Loading puntuaciones...")
        
    lista=[]
    fileobj=open(path+"\\ratings.csv", "r")
    next(fileobj)
    for line in csv.reader(fileobj, delimiter=";"):
        #lista.append(Puntuacion(occupationName=str(line.strip())))
        print(line)
    fileobj.close()
    #Occupation.objects.bulk_create(lista)  # bulk_create hace la carga masiva para acelerar el proceso
    
    #print("Occupations inserted: " + str(Occupation.objects.count()))
    print("---------------------------------------------------------")
'''
def populateLibro():
    print("Loading libros...")
    
    lista=[]
    fileobj=open(path+"\\bookfeatures.csv", "r")
    for line in fileobj.readlines():
        rip = str(line.strip()).split('|')
        if len(rip) != 2:
            continue
        lista.append(Genre(id=rip[1], genreName=rip[0]))
    fileobj.close()
    Genre.objects.bulk_create(lista)
    
    print("Genres inserted: " + str(Genre.objects.count()))
    print("---------------------------------------------------------")
'''  
       
# def populateRatings(u,m):
#     print("Loading ratings...")
#     Rating.objects.all().delete()

#     lista=[]
#     fileobj=open(path+"\\u.data", "r")
#     for line in fileobj.readlines():
#         rip = line.split('\t')
#         lista.append(Rating(user=u[int(rip[0].strip())], film=m[int(rip[1].strip())], rating=int(rip[2].strip()), rateDate= datetime.fromtimestamp(int(rip[3].strip())) ))
#     fileobj.close()
#     Rating.objects.bulk_create(lista)
#     print("Ratings inserted: " + str(Rating.objects.count()))
#     print("---------------------------------------------------------")
    
    
# def populateDatabase():
#     deleteTables()
#     populateOccupations()
#     populateGenres()
#     u=populateUsers()
#     m=populateFilms()
#     populateRatings(u,m)
#     print("Finished database population")
    
# if __name__ == '__main__':
#     populateDatabase()
