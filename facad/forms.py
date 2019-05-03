from django import forms
from dal import autocomplete

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
    
class weightForm(forms.Form):
	

	cgpa_weight = forms.FloatField(required=False)
	courses_weight = forms.FloatField(required=False)
	
			
			