# Generated by Django 3.2.8 on 2021-10-10 23:55

from django.db import migrations, models
import workflow_forms.models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_forms', '0005_uploaded_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploaded_file',
            name='uploaded_file',
            field=models.FileField(upload_to=workflow_forms.models.dirpath),
        ),
    ]