# Generated by Django 5.1.4 on 2024-12-17 22:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scholarship', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviewer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expertise', models.CharField(blank=True, max_length=255, null=True, verbose_name='Expertise')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Bio')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='as_reviewer', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Reviewer',
                'verbose_name_plural': 'Reviewers',
            },
        ),
        migrations.AlterField(
            model_name='applicationreview',
            name='reviewer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='scholarship.reviewer'),
        ),
    ]