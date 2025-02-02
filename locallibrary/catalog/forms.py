from django import forms
from django.forms import ModelForm
from catalog.models import BookInstance
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookModelForm(ModelForm):
    def clean_renewal_date(self):
        data = self.cleaned_data['due_back']

        # check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        
        # check if a date is in the allowed range (+4 weeks from today)

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        

        # Remember to always return the cleaned data

        return data
    class Meta:
        model = BookInstance
        # fields are the fields you want in the form
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
        