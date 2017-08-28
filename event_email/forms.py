from django import forms 
from .models import EmailTemplate

class EmailTemplateForm(forms.ModelForm):
	class Meta:
		model = EmailTemplate
		fields = '__all__' 
		widgets = {
			'html': forms.Textarea(attrs={'cols': 80, 'rows': 20})
			}