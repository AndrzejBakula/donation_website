from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128)


class Institution(models.Model):

    INSTITUTIONS = [
        (1, "fundacja"),
        (2, "organizacja pozarządowa"),
        (3, "zbiórka lokalna")
    ]

    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.IntegerField(choices=INSTITUTIONS, default=INSTITUTIONS[0][0])
    categories = models.ManyToManyField(Category)


