from django.db import models


class SimplePage(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=20)
    content = models.TextField()
