from django.db import migrations
from .. import models


def create_institution_1(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category = models.Category.objects.get(id=1)
    institution = Institution.objects.create(
        name='Fundacja #1',
        description='Fundacja testowa opis #1',
        type="Fundacja",
    )
    institution.save()
    institution.categories.add(category.id)
    institution.save()


def create_institution_2(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category = models.Category.objects.get(id=2)
    institution = Institution.objects.create(
        name='Fundacja #2',
        description='Fundacja testowa opis #2',
        type="Fundacja",
    )
    institution.save()
    institution.categories.add(category.id)
    institution.save()


def create_institution_3(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category = models.Category.objects.get(id=3)
    institution = Institution.objects.create(
        name='Fundacja #3',
        description='Fundacja testowa opis #3',
        type="Fundacja",
    )
    institution.save()
    institution.categories.add(category.id)
    institution.save()


def create_institution_4(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category = models.Category.objects.get(id=4)
    institution = Institution.objects.create(
        name='Fundacja #4',
        description='Fundacja testowa opis #4',
        type="Organizacja Pozarządowa",
    )
    institution.save()
    institution.categories.add(category.id)
    institution.save()


def create_institution_5(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category = models.Category.objects.get(id=1)
    institution = Institution.objects.create(
        name='Fundacja #5',
        description='Fundacja testowa opis #2',
        type="Organizacja Pozarządowa",
    )
    institution.save()
    institution.categories.add(category.id)
    institution.save()


def create_institution_6(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category_1 = models.Category.objects.get(id=1)
    category_2 = models.Category.objects.get(id=2)
    category_3 = models.Category.objects.get(id=3)
    category_4 = models.Category.objects.get(id=4)
    institution = Institution.objects.create(
        name='Fundacja #6',
        description='Fundacja testowa opis #6',
        type="Organizacja Pozarządowa",
    )
    institution.save()
    institution.categories.add(category_1.id)
    institution.categories.add(category_2.id)
    institution.categories.add(category_3.id)
    institution.categories.add(category_4.id)
    institution.save()


def create_institution_7(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category_2 = models.Category.objects.get(id=2)
    institution = Institution.objects.create(
        name='Fundacja #7',
        description='Fundacja testowa opis #7',
        type="Zbiórka Lokalna",
    )
    institution.save()
    institution.categories.add(category_2.id)
    institution.save()


def create_institution_8(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category_3 = models.Category.objects.get(id=3)
    institution = Institution.objects.create(
        name='Fundacja #8',
        description='Fundacja testowa opis #8',
        type="Zbiórka Lokalna",
    )
    institution.save()
    institution.categories.add(category_3.id)
    institution.save()


def create_institution_9_with_donation(apps, schema_editor):
    Institution = apps.get_model('projectapp', 'Institution')
    category_2 = models.Category.objects.get(id=2)
    category_3 = models.Category.objects.get(id=3)
    institution = Institution.objects.create(
        name='Fundacja #9',
        description='Fundacja testowa opis #9',
        type="Zbiórka Lokalna",
    )
    institution.save()
    institution.categories.add(category_2.id)
    institution.categories.add(category_3.id)
    institution.save()

    Donation = apps.get_model('projectapp', 'Donation')
    User = apps.get_model('auth', 'User')
    donation = Donation.objects.create(
        quantity=42,
        institution=institution,
        address='Adres testowy',
        phone_number='123456789',
        city='Testowo',
        zip_code='40-000',
        pick_up_date='2023-02-02',
        pick_up_time='11:30',
        pick_up_comment='Testowy Komentarz dotacji',
        user=User.objects.get(first_name='Test'),
        is_taken=True
    )
    donation.save()
    donation.categories.add(category_2.id)
    donation.save()


class Migration(migrations.Migration):
    dependencies = [
        ('projectapp', '0001_initial'),
        ('projectapp', '0002_users'),
        ('projectapp', '0003_example_category')
    ]

    operations = [
        migrations.RunPython(create_institution_1),
        migrations.RunPython(create_institution_2),
        migrations.RunPython(create_institution_3),
        migrations.RunPython(create_institution_4),
        migrations.RunPython(create_institution_5),
        migrations.RunPython(create_institution_6),
        migrations.RunPython(create_institution_7),
        migrations.RunPython(create_institution_8),
        migrations.RunPython(create_institution_9_with_donation),
    ]
