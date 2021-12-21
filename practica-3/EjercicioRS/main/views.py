import shelve
from main.models import Libro, Rating
from main.forms import UserForm, FilmForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  load_similarities
from main.populate import populateDatabase

def index(request): 
    return render(request,'index.html')

def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

def loadRS(request):
    load_similarities()
    return render(request,'loadRS.html')
 
# # APARTADO A
# # RS filtrado colaborativo basado en usuarios
# def recommendedFilmsUser(request):
#     if request.method=='GET':
#         form = UserForm(request.GET, request.FILES)
#         if form.is_valid():
#             idUser = form.cleaned_data['id']
#             user = get_object_or_404(UserInformation, pk=idUser)
#             shelf = shelve.open("dataRS.dat")
#             Prefs = shelf['Prefs']
#             shelf.close()
#             rankings = getRecommendations(Prefs,int(idUser))
#             recommended = rankings[:2]
#             films = []
#             scores = []
#             for re in recommended:
#                 films.append(Film.objects.get(pk=re[1]))
#                 scores.append(re[0])
#             items= zip(films,scores)
#             return render(request,'recommendationItems.html', {'user': user, 'items': items})
#     form = UserForm()
#     return render(request,'search_user.html', {'form': form})

# # APARTADO B
# # RS filtrado colaborativo basado en items
# def recommendedFilmUserItems(request):
#     if request.method=='GET':
#         form = UserForm(request.GET, request.FILES)
#         if form.is_valid():
#             idUser = form.cleaned_data['id']
#             user = get_object_or_404(UserInformation, pk=idUser)
#             shelf = shelve.open("dataRS.dat")
#             Prefs = shelf['Prefs']
#             SimilarItems = shelf['SimilarItems']
#             shelf.close()
#             rankings = getRecommendedItems(Prefs,SimilarItems,int(idUser))
#             recommended = rankings[:2]
#             films = []
#             scores = []
#             for re in recommended:
#                 films.append(Film.objects.get(pk=re[1]))
#                 scores.append(re[0])
#             items= zip(films,scores)
#             return render(request,'recommendationItems.html', {'user': user, 'items': items})
#     form = UserForm()
#     return render(request,'search_user.html', {'form': form})

# # APARTADO C
# # RS filtrado colaborativo basado en usuarios
# def similarFilms(request):
#     film = None
#     if request.method=='GET':
#         form = FilmForm(request.GET, request.FILES)
#         if form.is_valid():
#             idFilm = form.cleaned_data['id']
#             film = get_object_or_404(Film, pk=idFilm)
#             shelf = shelve.open("dataRS.dat")
#             ItemsPrefs = shelf['ItemsPrefs']
#             shelf.close()
#             recommended = topMatches(ItemsPrefs, int(idFilm),n=3)
#             films = []
#             similar = []
#             for re in recommended:
#                 films.append(Film.objects.get(pk=re[1]))
#                 similar.append(re[0])
#             items= zip(films,similar)
#             return render(request,'similarFilms.html', {'film': film,'films': items})
#     form = FilmForm()
#     return render(request,'search_film.html', {'form': form})

# #APARTADO D
# # RS filtrado colaborativo basado en items
# def recommendedUser(request):
#     if request.method=='GET':
#         form = FilmForm(request.GET, request.FILES)
#         if form.is_valid():
#             idFilm = form.cleaned_data['id']
#             film = get_object_or_404(Film, pk=idFilm)
#             shelf = shelve.open("dataRS.dat")
#             ItemsPrefs = shelf['ItemsPrefs']
#             shelf.close()
#             rankings = getRecommendations(ItemsPrefs,int(idFilm))
#             recommended = rankings[:3]
#             users = []
#             scores = []
#             for re in recommended:
#                 print(re)
#                 users.append(UserInformation.objects.get(pk=re[1]))
#                 scores.append(re[0])
#             items= zip(users,scores)
#             return render(request,'recommendationUsers.html', {'film': film, 'items': items})
#     form = UserForm()
#     return render(request,'search_film.html', {'form': form})


# #APARTADO E
# # RS filtrado colaborativo basado en usuarios
# def search(request):
#     if request.method=='GET':
#         form = UserForm(request.GET, request.FILES)
#         if form.is_valid():
#             idUser = form.cleaned_data['id']
#             user = get_object_or_404(UserInformation, pk=idUser)
#             return render(request,'ratedFilms.html', {'usuario':user})
#     form=UserForm()
#     return render(request,'search_user.html', {'form':form })



