from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Contact(models.Model):
    logo = models.ImageField(upload_to='logo')
    company_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    address_2 = models.CharField(max_length=250, blank=True)
    phone_number = PhoneNumberField(help_text='Contact phone number')
    email = models.EmailField(max_length=20)
    day_open = models.CharField(max_length=100, null=True)
    contact_note = models.TextField(null=True)

    def __str__(self):
        return self.company_name


class Socialmedia(models.Model):
    facebook = models.URLField(max_length=200)
    instagram = models.URLField(max_length=200)
    twitter = models.URLField(max_length=200)
    youtube = models.URLField(max_length=200, blank=True)


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,max_length=100,blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name






