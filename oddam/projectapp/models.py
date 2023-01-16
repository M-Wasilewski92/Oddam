from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


class Institution(models.Model):
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
