from django.contrib import admin
from main.models import Occupation,UserInformation,Film,Rating,Genre

admin.site.register(Occupation)
admin.site.register(UserInformation)
admin.site.register(Film)
admin.site.register(Rating)
admin.site.register(Genre)