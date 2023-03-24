from django.db import models
from django.urls import reverse
# Create your models here.

class Blog(models.Model):
    blog_title = models.CharField(max_length=200)
    blog_sub_title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='blog')
    slug = models.SlugField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.blog_title

    def get_url(self):
        return reverse('blog_detail', args=[self.slug])