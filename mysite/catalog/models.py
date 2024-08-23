from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.validators import FileExtensionValidator 
import uuid # Requerida para las instancias de libros únicos

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return  f"Nombre: {self.first_name} Apellidos: {self.last_name}"


class Usuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comentario = models.CharField(max_length=1000)
        

class Genre(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.name
        

class Book(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """

    title = models.CharField(max_length=200)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.

    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")

    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    genre = models.ManyToManyField(Genre, help_text="Seleccione un genero para este libro")
    portada = models.ImageField(upload_to='portadas', null=True, blank=True)
    
    video = models.FileField(upload_to='videos_uploaded',null=True, validators=[FileExtensionValidator(['MOV','avi','mp4','webm','mkv'])])
    pdf = models.FileField(upload_to='pdf_libros', null=True, blank=True) 
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.

    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.title


    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('book-detail', args=[str(self.id)])
    
    def display_genre(self):
        """
        Creates a string for the Genre. This is required to display genre in Admin.
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
    
    display_genre.short_description = 'Genre'

    def display_author(self):
        """
        Creates a string for the Author. This is required to display genre in Admin.
        """
        return self.author
    
    display_author.short_description = 'Auuttoorr'
        
        
class BookInstance(models.Model):
    """
    Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Can set book as returned"),)
        permissions = (("can_see_your_books", "Can see your borrowed books"),)
        
        #PERMISOS EXAMEN
        permissions = (("permibusca", "puede buscar libros"),)
        permissions = (("permiprestar", "puede prestar libros"),)
        permissions = (("permirenovar", "puede renovar libros"),)
        permissions = (("permidevolver", "puede devolver libros"),)

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        #return '%s (%s)' % (self.id,self.book.title)
        return self.book.title
    
    def display_book(self):
        return self.book.title
    
    display_book.short_description = "Book"
      
        
class Author(models.Model):
    """
    Modelo que representa un autor
    """
    #first_name = models.CharField(max_length=100, verbose_name="popeye")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    #date_of_death = models.DateField('Died', null=True, blank=True) #el 'Died' al principio no funciona con claves foraneas
    date_of_death = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.last_name, self.first_name)


"""""
    def display_books(self):
        books = Book.objects.filter(author_id = self.id)

        return books
    
    display_books.short_description = "Books"
"""
