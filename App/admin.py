from django.contrib import admin
from .models import Book,Genre,Category,Profile
from django.contrib.auth.models import User

#to display built in serchh bar in admin panel
class GenreAdmin(admin.ModelAdmin):
    search_fields=['title']

class CategoryAdmin(admin.ModelAdmin):
    search_fields=['name']

class BookAdmin(admin.ModelAdmin):
    search_fields=['title','author']
    

# Register your models here.
admin.site.register(Genre,GenreAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Profile)