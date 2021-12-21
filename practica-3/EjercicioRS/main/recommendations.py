#encoding:utf-8

from main.models import Libro,Rating
from collections import Counter
import shelve

def load_similarities():
    shelf = shelve.open('dataRS.dat')
    book_attr = books_attr()
    user_pref = user_preferences()
    shelf['similarities'] = compute_similarities(book_attr, user_pref)
    shelf.close()

def recommended_books(userId):
    shelf = shelve.open("dataRS.dat")
    read = set()
    read = set(a.libro for a in Rating.objects.filter(userId=userId))
    print('\nLibros leidos: ' + str(read))
    res = []
    print('\nSimiltudes: ' + str(shelf['similarities'][userId]))
    for idLibro, score in shelf['similarities'][userId]:
        if idLibro not in read:
            book = Libro.objects.get(pk=idLibro)
            res.append([book, 100 * score])
    shelf.close()
    print('\nLibros recomendados: ' + str(res[:3]))
    return res

def compute_similarities(book_attr, user_pref):
    print('Computing user-book similarity matrix')
    res = {}
    for u in user_pref:
        top_books = {}
        for a in book_attr:
            if(len(user_pref[u])>0):

                print('\nConjunto de preferencias de usuario: ' + str(user_pref[u][0]))
                print('Conjunto de atributos de libro: ' + str(set(book_attr[a])))
                top_books[a] = dice_coefficient(set(user_pref[u][0]), set(book_attr[a]))
        res[u] = Counter(top_books).most_common(10)
    return res

def books_attr():
    print('Computing the books attributes')
    books = {}
    
    for element in Libro.objects.all():
        book_id = element.idLibro
        autor = element.autor
        genero = element.genero
        idioma = element.idioma
        books.setdefault(book_id, [])
        books[book_id].append(autor)
        books[book_id].append(genero)
        books[book_id].append(idioma)
    return books

def user_preferences():
    print('Computing attributes from most common books for each user')
    users = {}
    for element in Rating.objects.all():
        userId = element.userId
        users.setdefault(userId, {})
        libro = element.libro
        if(element.rating>=4):
            users[userId][libro.idLibro] = [libro.autor,libro.genero,libro.idioma]
    for u in users:
        users[u] = [[attr[0], attr[1],attr[2]] for libro,attr in Counter(users[u]).most_common(1)]
    print('\nPreferencias de usuario: ' + str(users))
    return users

def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))