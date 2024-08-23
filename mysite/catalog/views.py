from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Book, Author, BookInstance, Genre, Usuario, Person
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author
from django.urls import reverse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.messages import get_messages
import datetime

from .forms import RenewBookForm, Formulario, CorreoForm, Buscar, Prestar
from django.contrib.auth.models import User
#from weasyprint import HTML, CSS
from django.template.loader import get_template
from django.core.files.base import ContentFile
from django.core.files import File
from django.http import JsonResponse
from django.forms.models import model_to_dict




#Formu BUSCAR
@permission_required('catalog.permibusca')
def buscarForm(request):

    if request.method == 'POST':
        form = Buscar(request.POST)
        libros = []

        if form.is_valid():
            titulo = form.cleaned_data['TITULO']
            prestatario = form.cleaned_data['prestatario']
            estado = form.cleaned_data['estado']

            if titulo == '' and prestatario == '' and estado == '':
                libros = BookInstance.objects.all()

            elif titulo != '' and prestatario == '' and estado == '':
                libros = BookInstance.objects.filter(book__title__contains = titulo)
                
            elif titulo != '' and prestatario != '' and estado == '':
                libros = BookInstance.objects.filter(book__title__contains = titulo).filter(borrower__username = prestatario)
                
            elif titulo != '' and prestatario != '' and estado != '':
                libros = BookInstance.objects.filter(book__title__contains = titulo).filter(borrower__username = prestatario).filter(status = estado)
                
            elif titulo == '' and prestatario != '' and estado == '':
                libros = BookInstance.objects.filter(borrower__username = prestatario)
            
            elif titulo == '' and prestatario != '' and estado != '':
                libros = BookInstance.objects.filter(borrower__username = prestatario).filter(status = estado)

            elif titulo == '' and prestatario == '' and estado != '':
                libros = BookInstance.objects.filter(status = estado)

            elif titulo != '' and prestatario == '' and estado != '':
                libros = BookInstance.objects.filter(book__title__contains = titulo).filter(status = estado)        
            	            
    else:
        form = Buscar()
        libros = []

    return render(request, 'buscar_form.html', {'form': form, 'libros': libros})



#Formu PRESTAR
@permission_required('catalog.permiprestar')
def prestarForm(request, pk):

    book_inst=get_object_or_404(BookInstance, pk = pk)
    fecha = datetime.date.today()
    fecha_default = datetime.date.today() + datetime.timedelta(weeks=4)
    
    if request.method == 'POST':
        form = Prestar(request.POST)
        #form.fields['retorno'].widget.attrs['readonly'] = True
        
        if form.is_valid():
            prestatario = form.cleaned_data['prestatario']
            
            num_prestados = BookInstance.objects.filter(borrower__username = prestatario).filter(status = 'o').count()

            if not prestatario:
                messages.error(request, 'Es obligatorio introducir el prestatario')
                          
            elif num_prestados >= 2:
                messages.error(request, 'Este prestatario ya tiene dos o más libros prestados')
            else:
                user = User.objects.get(username = prestatario)
                book_inst.borrower = user
                book_inst.status = 'o'
                book_inst.save()

                return redirect('buscar-form')

    else:
        form = Prestar(initial={'retorno': fecha_default,})
        #form.fields['retorno'].widget.attrs['readonly'] = True

    return render(request, 'prestar_form.html', {'form': form, 'book_inst': book_inst, 'fecha': fecha})



#Formu RENOVAR
@permission_required('catalog.permirenovar')
def renovarForm(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    if request.method == 'POST':

        form = RenewBookForm(request.POST)
        num_renovaciones = request.session.get(str(book_inst.pk), 0)

        if form.is_valid():

            print("Renovaciones DEL LIBRO " + str(book_inst.book) + " =  " +  str(num_renovaciones))

            #num_visits = request.session.get('num_visits', 0)
            #request.session['num_visits'] = num_visits + 1

            if num_renovaciones >= 3:
                messages.error(request, 'Este libro ya ha sido renovado 3 veces, no se puede renovar más')
            else:
                book_inst.due_back = form.cleaned_data['renewal_date']
                book_inst.save()
                request.session[str(book_inst.pk)] = num_renovaciones + 1
                num_renovaciones = request.session[str(book_inst.pk)]

                messages.success(request, 'Fecha de devolución renovada con éxito a ' + str(book_inst.borrower) + 
                             ' para el libro ' + str(book_inst.book) + ' a fecha: ' + str(form.cleaned_data['renewal_date']))
        

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        num_renovaciones = request.session.get(str(book_inst.pk), 0)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'renovar_form.html', {'form': form, 'book_inst':book_inst, 'num_renovaciones':num_renovaciones})



#@permission_required('catalog.permidevolver')
def Devolver(request, pk):
    book_inst=get_object_or_404(BookInstance, pk = pk)

    request.session[str(book_inst.pk)] = 0

    book_inst.status = 'a'
    book_inst.borrower = None
    book_inst.due_back = None
    book_inst.save()

    messages.success(request, 'El libro se ha devuelto exitosamente')

    return redirect('buscar-form')


















def get_author(request, pk):
    author = Author.objects.get(pk=pk)
    authors = Author.objects.all()
    #book = Book.objects.all()
    #data = {'title': book.title}
    #print(data)
    return JsonResponse(list(authors.values()), safe=False)
    #return JsonResponse(model_to_dict(author))


def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    
    # Genera contadores de algunos de los objetos principales
    num_books=Book.objects.all().count()
    num_instances=BookInstance.objects.all().count()
    # Libros disponibles (status = 'a')
    num_instances_available=BookInstance.objects.filter(status__exact='a').count()
    num_authors=Author.objects.count()  # El 'all()' esta implícito por defecto.
    num_generos= Genre.objects.all().count()
    num_libros = Book.objects.filter(title__icontains='el').count()
    lista=["nombre uno", "nombre dos","nombre tres"]
    libros = Book.objects.all()
    
    #ver todos los valores que hay en el diccionario junto con sus claves
    for clave, valor in request.session.items():
        print(f'Clave: {clave}, Valor: {valor}')

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    """ if num_visits % 2 == 0:
        messages.add_message(request=request, level=messages.INFO, message='Mensaje uno de INFO')
        messages.add_message(request=request, level=messages.DEBUG, message='Mensaje uno de DEBUG')
        messages.add_message(request=request, level=messages.ERROR, message='Mensaje uno de ERROR')
        messages.add_message(request=request, level=messages.WARNING, message='Mensaje uno de WARNING')
        messages.add_message(request=request, level=messages.SUCCESS, message='Mensaje uno de SUCCESS')
        messages.info(request, 'Mensaje dos de INFO') """


    # Renderiza la plantilla HTML index.html con los datos en la variable contexto
    return render(
        request,
        'index.html',
        context={'num_books':num_books,'num_instances':num_instances,'num_instances_available':num_instances_available,
                 'num_authors':num_authors, 'num_generos':num_generos, 'num_libros':num_libros, "lista":lista, 
                 "libros":libros, 'num_visits':num_visits,}
    )


def probando(request, id):
    libro = Book.objects.get(pk=id)

    return render(
        request,
        'probando.html',
        context={"libro":libro}
    )

def autores(request, id):
    autor=Author.objects.get(pk=id)

    return render(
        request,
        'autores.html',
        context={"autor":autor}
    )


#CLACULATOR
def resuelve(request):
    resul = eval(request.session.get('num'))
    return resul

#@login_required
#@permission_required('catalog.can_mark_returned')
def calculator(request, valor=''):
    resultado = ''

    if (valor == 'div'):
        valor = '/'

    if (valor == 'C'):
        request.session['num'] = ''
    
    elif (valor == 'X'):
        request.session['num'] = request.session['num'][:-1]

    elif (valor == '='):
        resultado = resuelve(request)
        resultado = '=' + str(resultado)
        #request.session['num'] = ''
    else:
        request.session['num'] = request.session.get('num', '') + valor
        print('Diccionario ' + request.session['num'])
        #request.session['num'] = ''

    #request.session.modified = True

    return render(
        request,
        'calculator.html',
        context={"operacion": request.session.get('num'), 'resultado': resultado}
    )



#LIST VIEWS
class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # Llame primero a la implementación base para obtener un contexto.
        context = super(BookListView, self).get_context_data(**kwargs)
        # Obtenga el blog del id y agréguelo al contexto.
        context['some_data'] = 'Estos son solo algunos datos'
        return context
    

class AuthorListView(generic.ListView):
    model = Author
    


#DETAIL VIEWS
class BookDetailView(generic.DetailView):
    model = Book

class AuthorDetailView(generic.DetailView):
    model = Author


#Vista genérica basada en clases que enumera los libros prestados al usuario actual
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    

#Vista de todos los libros prestados
class LoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')
    
    

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()
            messages.success(request, 'Fecha de devolución renovada con éxito a ' + str(book_inst.borrower) + 
                             ' para el libro ' + str(book_inst.book) + ' a fecha: ' + str(form.cleaned_data['renewal_date']))

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))
            
        #messages.error(request, 'Por favor complete correctamente todos los campos')
            
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})
    



#Formulario Correo
def correoForm(request):
    if request.method == 'POST':
        form = CorreoForm(request.POST,request.FILES)
        file = request.FILES['archivo']
        print("wwwwwwwwwwwwwww")
        print(file.name)
        print(file.size)
        print(file.content_type)

        if form.is_valid():
            destinatario = form.cleaned_data['destinatario']
            asunto = form.cleaned_data['asunto']
            mensaje = form.cleaned_data['mensaje']
            file = form.cleaned_data['archivo']
            #file = request.FILES.getlist('archivo')

            email = EmailMessage(asunto, mensaje, "1817826@alu.murciaeduca.es", [destinatario])
            email.attach(file.name, file.read(), file.content_type)
            #email.send()

        return HttpResponseRedirect(reverse('index'))
    else:
        form = CorreoForm()

    return render(request, 'correo_form.html', {'form': form})
    
    

#Ejercicio Formulario
def formulario(request):

    if request.method == 'POST':
        form = Formulario(request.POST)

        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            ape = form.cleaned_data['apellido']
            edad = form.cleaned_data['edad']

            if 'agregar' in request.POST:

                if not Person.objects.filter(first_name= nombre, last_name=ape, age=edad).exists():
                    Person.objects.create(first_name= nombre, last_name=ape, age=edad)
                    messages.success(request, 'Persona agregada con éxito')
                else:
                    messages.error(request, 'La persona que quiere agregar ya existe')
                    return redirect ('formulario')
            
            if 'borrar' in request.POST:

                if Person.objects.filter(first_name= nombre, last_name=ape, age=edad).exists():
                    persona = Person.objects.get(first_name= nombre, last_name=ape, age=edad)
                    persona.delete()
                    messages.success(request, 'Persona borrada con éxito')
                else:
                    messages.error(request, 'La persona que quiere borrrar no existe')

                    #return redirect(request.get_full_path()) Me hace un redirect a la página en la que me encuentro.
                    return redirect ('formulario')

            return HttpResponseRedirect(reverse('index'))       
    else:
        #form = Formulario()
        form = Formulario(initial={'nombre':'Paco', 'apellido':'Pérez'})
        #messages.info(request, 'hola, buenos días')

    return render(request, 'formulario.html', {'form': form})



def pdf_generation(request, pk):
    
    if request.method == 'POST':
        book = get_object_or_404(Book, pk = pk)
        context = {'book': book}
        
        html_template = get_template('pdf_libros.html')
        html_content = html_template.render(context)
        
        #pdf_file = HTML(string=html_content).write_pdf()
        pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf') 
        response['Content-Disposition'] = f'filename={book.title}.pdf'

        book.pdf.save(f'{book.title}.pdf', ContentFile(response.getvalue()))

        #return response
        return redirect(f'/catalog/book/{book.pk}')

    return render(request, 'catalog/book_detail.html', {'book': book})




#CRUD de Autores y Libros
class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'
    initial={'date_of_death':'05/01/2018',}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('authors')


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = '__all__'

class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    fields = ['title','summary','genre','portada', 'video', 'pdf']

class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    permission_required = 'catalog.can_mark_returned'
    success_url = reverse_lazy('books')





#formulario con varios campos. Nombre, apellidos y edad a la base de datos al hecr submit

#hacer transferencias. Implica dos tablas


#lista con los libros y el nombre del autor al lado
# montar un url con la id o pk del libro, La Tabla de Flandes Arturo/catalog/probando/1
# crear la funcion probando aqui, que recibira un parametro
#libro:(libro) autor:(autor)


#crear una tabla.  tendremos los usuarios que van a trabajar en catalog. Django tirnr una tabla con los usuarios de django.
#los usuarios de catalog son usuarios de django. Aparte de los datos del usuario de django añadir un campo comnetario
#relate-name
