from django.db import models

# Create your models here.
class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True,max_length=100,blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name
