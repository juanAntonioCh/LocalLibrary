from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from .models import BookInstance, Book
from django.contrib.auth.models import User
import datetime


class Buscar(forms.Form):
    TITULO = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    
    presta = User.objects.all()
    LISTA_PRESTA = [(None, '-----')]

    for p in presta:
        LISTA_PRESTA.append((p, p))

    LISTA_PRESTA = tuple(LISTA_PRESTA)
    
    prestatario = forms.ChoiceField(choices = LISTA_PRESTA, required=False)
    
    LOAN_STATUS = (
    	(None, '----'),
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    
    estado = forms.ChoiceField(choices = LOAN_STATUS, required=False)



class Prestar(forms.Form):

    retorno = forms.DateField(widget=forms.DateInput(attrs={'readonly': 'readonly'}),required=False)
    
    presta = User.objects.all()
    LISTA_PRESTA = [(None, '-----')]

    for p in presta:
        LISTA_PRESTA.append((p, p))

    LISTA_PRESTA = tuple(LISTA_PRESTA)
    
    prestatario = forms.ChoiceField(choices = LISTA_PRESTA, required=False)

    def clean_prestatario(self):
        presta = self.cleaned_data['prestatario']

        if not presta:
            raise ValidationError(_('El prestatario no puede estar vacio'))

        return presta
    



class Renovar(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    
    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data




#para renovar la fecha de devolución de un libro
class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
    

#para renovar la fecha de devolución de un libro basándose en el modelo de libro
class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
       data = self.cleaned_data['due_back']

       #Check date is not in past.
       if data < datetime.date.today():
           raise ValidationError(_('Invalid date - renewal in past'))

       #Check date is in range librarian allowed to change (+4 weeks)
       if data > datetime.date.today() + datetime.timedelta(weeks=4):
           raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

       # Remember to always return the cleaned data.
       return data

    class Meta:
        model = BookInstance
        fields = ['due_back',]
        labels = { 'due_back': _('Renewal date'), }
        help_texts = { 'due_back': _('Enter a date between now and 4 weeks (default 3).'), }





class CorreoForm(forms.Form):
    destinatario = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    asunto = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    mensaje = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}))
    archivo = forms.FileField()
    #archivos = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))

    
	

class Formulario(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), required=False)
    edad = forms.IntegerField(required=False)

    TIPO_MASCOTA = [
        ('perro', 'Perro'),
        ('gato', 'Gato'),
        ('tortuga', 'Tortuga'),
        ('loro', 'Loro'),
    ]

    mascota = forms.MultipleChoiceField(
        choices = TIPO_MASCOTA, 
        widget=forms.SelectMultiple,
        required=False)
    
    TIPO_OCIO = [
        ('cine', 'Cine'),
        ('musica', 'Música'),
    ]

    ocio = forms.MultipleChoiceField(
        choices=TIPO_OCIO,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    SEXOS = [
        ('hombre', 'Hombre'),
        ('mujer', 'Mujer'),
    ]

    sexo = forms.ChoiceField(
        choices=SEXOS,
        widget=forms.RadioSelect,
        required=False,
    )

    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
    )

    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type':'time'}),
        required=False
    )

    TIPO_COLOR = (
        ('azul', 'Azul'),
        ('rojo', 'Rojo'),
        ('verde', 'Verde'),
        ('negro', 'Negro')
    )

    color = forms.ChoiceField(choices = TIPO_COLOR, required=False)

    libros = Book.objects.all()
    LISTA_LBROS = [(None, '-----')]

    for libro in libros:
        LISTA_LBROS.append((libro, libro))

    LISTA_LBROS = tuple(LISTA_LBROS)

    libro = forms.ChoiceField(choices = LISTA_LBROS, required=False)


    observacion = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'Please enter the description'}),
        required=False
    )



#Insertar videos y ficheros(PDF que hay que generar) en un formulario
#varios botones submit que harán diferentes cosas.
#le doy a un boton que me genera un pdf con el contenido del libro y lo incluye en un campo del modelo de libro.

""" {% for fiel in form%}
    {% if field.errors %}
        {% for error in field.errors %}

        {% endfor %}

    {% endif %}
{% endfor %} """
