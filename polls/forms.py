from django import forms
from dal import autocomplete

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
    
class AddEntryForm(forms.Form):
	fid = forms.IntegerField()
	title = forms.CharField()
	description = forms.CharField()
	cgpa = forms.IntegerField()
	cgpa_weight = forms.IntegerField()
	courses_weight = forms.IntegerField()
	count = forms.IntegerField()


	def __init__(self, tup, *args, **kwargs):
		# extra_fields = kwargs.pop('extra', 0)
		super(AddEntryForm, self).__init__(*args, **kwargs)
		self.fields['courses'] = autocomplete.Select2ListChoiceField(
        choice_list=tup,
        widget=autocomplete.ListSelect2(url=None)
    )


	def clean_cgpa(self):
		data = self.cleaned_data['cgpa']
		if not (int(data)>=1 and int(data)<=10):
			raise ValidationError(_('Invalid cgpa'))

		return data

	def clean_cgpa_weight(self):
		data = self.cleaned_data['cgpa_weight']
		if not (int(data)>=0 and int(data)<=1):
			raise ValidationError(_('Invalid cgpa weight'))

		return data

	def clean_courses_weight(self):
		data = self.cleaned_data['courses_weight']
		if not (int(data)>=0 and int(data)<=1):
			raise ValidationError(_('Invalid courses weight'))

		return data
			
			