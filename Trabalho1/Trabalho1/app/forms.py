"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

#formulario de adcionar dados na triple store
class addTripleStore(forms.Form):
    Sujeito = forms.CharField(max_length=255)
    Predicado = forms.CharField(max_length=255)
    Objecto = forms.CharField(max_length=255)
#formulario para remover dados na triple store
class removeTripleStore(forms.Form):
    sujeito = forms.CharField(max_length=255)
    predicado = forms.CharField(max_length=255)
    objecto = forms.CharField(max_length=255)
#formulario para pesquisar dados na triple store
class pesquisarTripleStore(forms.Form):
    sujeito = forms.CharField(max_length=255)
    predicado = forms.CharField(max_length=255)
    objecto = forms.CharField(max_length=255)
#class gameSelectChoices(forms.Form):
#   def __init__(self, *args, **kwargs):
#       choices = kwargs.pop('my_choices')
#       super(MyCustomForm, self).__init__(*args, **kwargs)
#       self.fields["my_field"] = forms.ChoiceField(choices=choices)
#   
#   other_field = forms.CharField()