from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import Author, Genre, Book, BookInstance, Usuario

# Register your models here.

#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Permission)
#admin.site.register(Usuario)
#admin.site.register(BookInstance)

# Define the admin class
class AuthorInstanceInline(admin.TabularInline): #para poder ver en la vista de cada autor todos los libros de este
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death') #VISTA GENERAL DE LOS LIBROS
    fields = ('last_name', 'first_name', ('date_of_birth', 'date_of_death')) #VISTA DE CADA LIBRO 
    inlines = [AuthorInstanceInline] #para que se vea lo de arriba 'class AuthorInstanceInline'

# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)


# Register the Admin classes for Book using the decorator

class BooksInstanceInline(admin.TabularInline): #para poder ver en la vista de cada libro todas las instancias de este
    model = BookInstance


@admin.register(Book)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_author', 'display_genre')
    inlines = [BooksInstanceInline]

# Register the Admin classes for BookInstance using the decorator

@admin.register(BookInstance)

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

