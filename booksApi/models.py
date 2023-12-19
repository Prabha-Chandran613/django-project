from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True, default='0000')

    def __str__(self):
        return self.title
