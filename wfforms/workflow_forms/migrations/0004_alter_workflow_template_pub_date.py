# Generated by Django 3.2.8 on 2021-10-10 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflow_forms', '0003_alter_workflow_template_workflow_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflow_template',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Date published'),
        ),
    ]
