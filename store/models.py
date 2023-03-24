from django.db import models
from category.models import Category
from django.urls import reverse


# Create your models here.
Labels = (('new','New'),('hot','Hot'),('sale','Sale'),('','Default'))

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    labels = models.CharField(max_length=100, choices=Labels, blank=True)
    price = models.IntegerField()
    discount_price = models.IntegerField()
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    # category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('single_product_view', args=[self.category.slug, self.slug])
