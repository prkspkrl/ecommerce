# Generated by Django 4.1.1 on 2023-02-09 16:16

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(help_text='Contact phone number', max_length=128, region=None)),
                ('email', models.EmailField(max_length=15, null=True)),
                ('address', models.CharField(max_length=20)),
                ('address2', models.CharField(max_length=50, null=True)),
                ('delivery_day', models.CharField(max_length=20, null=True)),
                ('note', models.TextField()),
            ],
        ),
    ]