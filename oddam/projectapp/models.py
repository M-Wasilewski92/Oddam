from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
     Category name are represented by this model.
    """
    name = models.CharField(max_length=50)


class Institution(models.Model):
    """
         Institutions information's are stored by this model.

    """
    TYPE_OF_INSTITUTION_CHOICES = [
        ('Fundacja', 'Fundacja'),
        ('Organizacja Pozarządowa', 'Organizacja Pozarządowa'),
        ('Zbiórka Lokalna', 'Zbiórka Lokalna')
    ]
    name = models.CharField(max_length=50)
    description = models.TextField()
    type = models.CharField(
        max_length=40,
        choices=TYPE_OF_INSTITUTION_CHOICES,
        default='Fundacja',
    )
    categories = models.ManyToManyField(Category)


class Donation(models.Model):
    """
       Donations information's are stored in this model.

    """
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    city = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField(blank=True)
    pick_up_time = models.DateTimeField(blank=True)
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
