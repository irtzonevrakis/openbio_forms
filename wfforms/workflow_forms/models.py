from django.db import models
from uuid import uuid4
from os import path

def dirpath(instance, filename):
    # Avoid file injection attacks by completely disregarding
    # provided path when storing to filesystem. Join two uuids instead.
    return path.join(str(uuid4()), str(uuid4()))
class Workflow_Template(models.Model):
    workflow_name = models.CharField(max_length=64, null=True, unique=True)
    workflow_yaml = models.TextField() # Workflow Argo yaml
    workflow_custform = models.TextField() # Workflow form decriptor
    pub_date = models.DateTimeField('Date published', auto_now_add=True)
class Uploaded_File(models.Model):
    fname = models.CharField(max_length=512, null=True) # Uploaded filename
    uid = models.UUIDField() # Run key / UUID
    uploaded_file = models.FileField(upload_to=dirpath) # Server upload path
