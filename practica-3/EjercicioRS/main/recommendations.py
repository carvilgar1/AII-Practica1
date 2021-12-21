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

# def recommended_books(user):
#     shelf = shelve.open("dataRS.dat")
#     #conjunto de artistas que ya ha escuchado el usuario, que no se consideran para recomendar
#     listened = set()
#     listened = set(a.artist.id for a in UserArtist.objects.filter(user=user))
#     res = []
#     for artist_id, score in shelf['similarities'][user]:
#         if artist_id not in listened:
#             artist_name = Artist.objects.get(pk=artist_id).name
#             res.append([artist_name, 100 * score])
#     shelf.close()
#     print(res)
#     return res

def compute_similarities(book_attr, user_pref):
    print('Computing user-book similarity matrix')
    res = {}
    for u in user_pref:
        top_books = {}
        for a in book_attr:
            top_books[a] = dice_coefficient(user_pref[u], book_attr[a])
        res[u] = Counter(top_books).most_common(10)
    return res

def books_attr():
    print('Computing the books attributes')
    books = {}
    
    for element in Libro.objects.all():
        book_id = element.id
        autor = element.autor
        genero = element.genero
        idioma = element.idioma
        books.setdefault(book_id, [])
        books[book_id].append(autor,genero,idioma)
    return books

def user_preferences():
    print('Computing attributes from most common books for each user')
    users = {}
    for element in Rating.objects.all():
        userId = element.userId
        users.setdefault(userId, {})
        libro = element.libro
        if(element.rating>=4):
            users[userId][libro.id] = [libro.autor,libro.genero,libro.idioma]
    for u in users:
        users[u] = [[autor,genero,idioma] for libro,autor,genero,idioma in Counter(users[u]).most_common(5)]
    return users

def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))