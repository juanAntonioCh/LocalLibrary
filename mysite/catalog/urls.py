#from django.conf.urls import url
from django.urls import path
from django.urls import re_path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('probando/<int:id>/', views.probando,name='probando'),
    path('autores/<int:id>/', views.autores,name='autores'),
    path('index/',views.index,name='index'),
    path('calculator/', views.calculator,name='calculator'),
    #path('calculator/', login_required(views.calculator),name='calculator'),
    path('calculator/<str:valor>/', views.calculator,name='calculator'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/', views.LoanedBooksListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('formulario/', views.formulario, name='formulario'),
    path('correo/',views.correoForm, name='correo-form'),
    path('pdf/<int:pk>', views.pdf_generation, name='pdf'),
    path('aauthor/<int:pk>', views.get_author,name='author')
    #re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
]

#EXAMEN
urlpatterns += [
    path('buscar/',views.buscarForm, name='buscar-form'),
    path('prestar/<uuid:pk>',views.prestarForm, name='prestar-form'),
    path('renovar/<uuid:pk>',views.renovarForm, name='renovar-form'),
    path('devolver/<uuid:pk>',views.Devolver, name='devolver'),
]

urlpatterns += [
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]

urlpatterns += [
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
]



