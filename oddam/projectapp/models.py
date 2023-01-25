from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
     Category name are represented by this model.
    """
    name = models.CharField(max_length=50, verbose_name='Kategorie')

    class Meta:
        verbose_name = 'kategoria'
        verbose_name_plural = 'kategorie'

    def __str__(self):
        return self.name


class Institution(models.Model):
    """
         Institutions information's are stored by this model.

    """
    TYPE_OF_INSTITUTION_CHOICES = [
        ('Fundacja', 'Fundacja'),
        ('Organizacja Pozarządowa', 'Organizacja Pozarządowa'),
        ('Zbiórka Lokalna', 'Zbiórka Lokalna')
    ]
    name = models.CharField(max_length=50, verbose_name='Nazwa Instytucji')
    description = models.TextField(verbose_name='Opis')
    type = models.CharField(
        max_length=40,
        choices=TYPE_OF_INSTITUTION_CHOICES,
        default='Fundacja',
        verbose_name='Rodzaj Fundacji'
    )
    categories = models.ManyToManyField(Category, verbose_name='Kategorie')

    class Meta:
        verbose_name = 'instytucja'
        verbose_name_plural = 'instytucje'

    def __str__(self):
        return self.name


class Donation(models.Model):
    """
       Donations information's are stored in this model.

    """
    quantity = models.PositiveIntegerField(verbose_name='Ilość darów')
    categories = models.ManyToManyField(Category, verbose_name='Kategorie')
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name='Instytucja')
    address = models.CharField(max_length=50, verbose_name='Adres')
    phone_number = models.CharField(max_length=15, verbose_name='Numer Telefonu')
    city = models.CharField(max_length=30, verbose_name='Miasto')
    zip_code = models.CharField(max_length=10, verbose_name='Kod pocztowy')
    pick_up_date = models.DateField(blank=True, verbose_name='Data odbioru')
    pick_up_time = models.TimeField(blank=True, verbose_name='Godzina odbioru')
    pick_up_comment = models.TextField(verbose_name='Komentarz')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Użytkownik')
    is_taken = models.BooleanField(default=False, null=True, verbose_name='Datek przekazany')

    class Meta:
        verbose_name = 'dotacja'
        verbose_name_plural = 'dotacje'

    def __str__(self):
        return self.pick_up_comment
