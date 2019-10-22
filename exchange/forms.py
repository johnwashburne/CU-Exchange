from django import forms
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from .models import TicketOffering, Game
from django.contrib.auth.forms import UserCreationForm


class SellForm(forms.Form):

    game = forms.ModelChoiceField(queryset=Game.objects.all())
    HILL = 'Hill'
    UPPER = 'Upper'
    LOWER = 'Lower'

    LOCATION_CHOICES = (
        (HILL, 'Hill'),
        (UPPER, 'Upper Deck'),
        (LOWER, 'Lower Deck'),
    )

    location = forms.CharField(max_length=6, widget=forms.Select(choices=LOCATION_CHOICES))
    price = forms.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('5.00'))])
    
    
class UserCreateForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        
