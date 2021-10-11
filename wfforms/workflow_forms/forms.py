from django import forms
from yaml import safe_load, safe_dump
from .argo_parametrizer.fd_parser import parse_field_tsv
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from .models import Workflow_Template

class UploadForm(forms.ModelForm):
    class Meta:
        model = Workflow_Template
        fields = ['workflow_name', 'workflow_yaml', 'workflow_custform']

    def clean_workflow_yaml(self):
        try:
            data = self.cleaned_data['workflow_yaml']
            safe_load(data)
        except:
            raise ValidationError(_('Invalid workflow yaml!'))
        return data
    
    def clean_workflow_custform(self):
        try:
            data = self.cleaned_data['workflow_custform']
            parse_field_tsv(data)
        except ValueError as ve:
            raise ValidationError(_(f'Invalid field description: {ve}'))
        except BaseException as e:
            print(e)
            raise ValidationError(_('An unknown error occured'))
        return data

