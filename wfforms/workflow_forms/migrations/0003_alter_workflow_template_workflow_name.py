# Generated by Django 3.2.8 on 2021-10-10 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_forms', '0002_workflow_template_workflow_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow_template',
            name='workflow_name',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]
