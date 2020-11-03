from django.db import models
from django.contrib.auth.models import User


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


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=24)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=24)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)