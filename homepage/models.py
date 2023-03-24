from django.db import models

# Create your models here.
class Slider(models.Model):
    title = models.CharField(max_length=250)
    sub_title = models.CharField(max_length=250)
    description = models.TextField(max_length=500)
    cta = models.CharField(max_length=250,blank=True)
    slug = models.SlugField(max_length=200,unique=True)
    image = models.ImageField(upload_to='photos/slider')
    is_active = models.BooleanField(default=True)
    position = models.IntegerField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title

class Whyus(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.title

class Brand (models.Model):
    brand_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='photos/brand')

    def __str__(self):
        return self.brand_name
