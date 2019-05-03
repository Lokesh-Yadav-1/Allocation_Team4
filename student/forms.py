from django import forms
from dal import autocomplete

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class GivePref(forms.Form):
	
	def __init__(self, projects, n,  *args, **kwargs):
		super(GivePref, self).__init__(*args, **kwargs)
		for i in range(0,n):
			self.fields[projects[i]] = forms.IntegerField()
			