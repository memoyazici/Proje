from django.db import models


# Create your models here.

class Post(models.Model):
    author = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.image.url

