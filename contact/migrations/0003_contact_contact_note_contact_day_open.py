# Generated by Django 4.1.1 on 2023-02-03 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0002_alter_contact_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='contact_note',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='day_open',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
