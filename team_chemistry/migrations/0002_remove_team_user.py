# Generated by Django 4.2.4 on 2023-10-10 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team_chemistry', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='user',
        ),
    ]
