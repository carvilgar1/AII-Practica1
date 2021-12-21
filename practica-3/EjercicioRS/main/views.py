import shelve
from main.models import Libro, Rating
from main.forms import UserForm, FilmForm
from django.shortcuts import render, get_object_or_404
from main.recommendations import  load_similarities,recommended_books
from main.populate import populateDatabase

def index(request): 
    return render(request,'index.html')

def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')

def loadRS(request):
    load_similarities()
    return render(request,'loadRS.html')
 
def recommendedBooks(request):
    form = UserForm(request.GET, request.FILES)
    if form.is_valid():
        user = form.cleaned_data['id']
        books = recommended_books(int(user))
        params = {'form': form, 'user':user,'books': books}
    else:
        params = {'form': UserForm()}
    return render(request,'recommendedBooks.html', params)