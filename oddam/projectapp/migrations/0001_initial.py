# Generated by Django 4.1.5 on 2023-02-10 16:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Kategorie')),
            ],
            options={
                'verbose_name': 'kategoria',
                'verbose_name_plural': 'kategorie',
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nazwa Instytucji')),
                ('description', models.TextField(verbose_name='Opis')),
                ('type', models.CharField(choices=[('Fundacja', 'Fundacja'), ('Organizacja Pozarządowa', 'Organizacja Pozarządowa'), ('Zbiórka Lokalna', 'Zbiórka Lokalna')], default='Fundacja', max_length=40, verbose_name='Rodzaj Fundacji')),
                ('categories', models.ManyToManyField(to='projectapp.category', verbose_name='Kategorie')),
            ],
            options={
                'verbose_name': 'instytucja',
                'verbose_name_plural': 'instytucje',
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Ilość darów')),
                ('address', models.CharField(max_length=50, verbose_name='Adres')),
                ('phone_number', models.CharField(max_length=15, verbose_name='Numer Telefonu')),
                ('city', models.CharField(max_length=30, verbose_name='Miasto')),
                ('zip_code', models.CharField(max_length=10, verbose_name='Kod pocztowy')),
                ('pick_up_date', models.DateField(blank=True, verbose_name='Data odbioru')),
                ('pick_up_time', models.TimeField(blank=True, verbose_name='Godzina odbioru')),
                ('pick_up_comment', models.TextField(verbose_name='Komentarz')),
                ('is_taken', models.BooleanField(default=False, null=True, verbose_name='Datek przekazany')),
                ('categories', models.ManyToManyField(to='projectapp.category', verbose_name='Kategorie')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectapp.institution', verbose_name='Instytucja')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik')),
            ],
            options={
                'verbose_name': 'dotacja',
                'verbose_name_plural': 'dotacje',
            },
        ),
    ]
