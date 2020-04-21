from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    text = models.TextField()

    def __str__ (self):
        return f"{self.title} - {self.text}"
