# Generated by Django 5.1.4 on 2024-12-19 12:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0004_remove_scholarshipapplication_reviewers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scholarship',
            name='target_audience',
        ),
    ]