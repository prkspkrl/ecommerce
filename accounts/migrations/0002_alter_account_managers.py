# Generated by Django 4.1.1 on 2023-02-09 19:33

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='account',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]