from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from workflow_forms.models import Workflow_Template, Uploaded_File
from workflow_forms.forms import UploadForm
from datetime import date
from .wf_dynamic_form import get_django_form_from_tsv

from .argo_parametrizer.argo_parametrizer import *

from .secrets import *

import requests

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UploadForm()
    
    context = {'form': form}

    return render(request, 'form.html', context)

from uuid import uuid4, UUID

def render_form(request, workflow_name):
    workflow_instance = get_object_or_404(Workflow_Template, 
                                          workflow_name=workflow_name)
    form = get_django_form_from_tsv(workflow_instance.workflow_custform)
    if request.method == 'POST':
        form = form(request.POST, request.FILES)
        if form.is_valid():
            run_key = uuid4()
            cd = form.cleaned_data
            wf = ArgoWF(workflow_instance.workflow_yaml)
            if request.FILES:
                wf.add_obc_download_preamble()
                for k in request.FILES.keys():
                    record = Uploaded_File(fname=k,
                                           uid=run_key,
                                           uploaded_file=request.FILES[k])
                    record.save()
                    wf.add_obc_file_download(run_key,
                                             k,
                                             request._current_scheme_host)
            variables = [{'name': 'RUN_KEY', 'value': str(run_key)}]
            for k in cd.keys():
                if type(cd[k]) == int or type(cd[k]) == float or type(cd[k]) == str:
                    variables.append({'name': k, 'value': str(cd[k])})
            wf.add_argo_variables(variables)
            headers = {'Authorization': argo_token,
                       'content-type': 'application/json'}
            r = requests.post(f'{argo_server}/api/v1/workflows/{argo_namespace}',
                              data=wf.dump_json_for_argo_api(), # XXX Argo API only accepts JSON
                              headers=headers)
            if r.status_code == 200:
                response = HttpResponse('Workflow submitted successfully!')
            else:
                response = HttpResponse('Failed X_X\n'+r.text)
            return response
            '''response = HttpResponse(wf_yaml, content_type='application/x-yaml')
            response['Content-Disposition'] = f'inline; filename={workflow_name}_mod.yaml'
            return response'''

    context = {'form': form}

    return render(request, 'form.html', context)

def get_file(request, uid, fname):
    file_instance = get_object_or_404(Uploaded_File, 
                                      uid=UUID(uid),
                                      fname=fname)
    response = HttpResponse(file_instance.uploaded_file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'inline; filename={file_instance.fname}'
    return response

