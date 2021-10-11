import django.forms
from .argo_parametrizer.fd_parser import parse_field_tsv

def get_django_fields_from_dictl(diclist):
    django_fields = {}
    for dic in diclist:
        if dic['type'] == 'str':
            f = django.forms.CharField(label=dic['descr'],
                                       initial=dic['default_value'],
                                       max_length=dic['lim_max'])
        if dic['type'] == 'int':
            f = django.forms.IntegerField(label=dic['descr'],
                                          initial=dic['default_value'],
                                          min_value=dic['lim_min'],
                                          max_value=dic['lim_max'])
        if dic['type'] == 'float':
            f = django.forms.FloatField(label=dic['descr'],
                                          initial=dic['default_value'],
                                          min_value=dic['lim_min'],
                                          max_value=dic['lim_max'])
        if 'file' in dic['type']:
            f = django.forms.FileField(label=dic['descr'])
        django_fields[dic['stored_name']] = f
    return django_fields

def get_django_form_from_tsv(tsv):
    fields = get_django_fields_from_dictl(parse_field_tsv(tsv))
    return type('WfForm', (django.forms.Form,), fields)
