from django.db import migrations


def create_categories_1(app, schema_editor):
    Category = app.get_model('projectapp', 'Category')
    category = Category.objects.create(
        name=f'#1'
    )
    category.save()


def create_categories_2(app, schema_editor):
    Category = app.get_model('projectapp', 'Category')
    category = Category.objects.create(
        name=f'#2'
    )
    category.save()


def create_categories_3(app, schema_editor):
    Category = app.get_model('projectapp', 'Category')
    category = Category.objects.create(
        name=f'#3'
    )
    category.save()


def create_categories_4(app, schema_editor):
    Category = app.get_model('projectapp', 'Category')
    category = Category.objects.create(
        name=f'#4'
    )
    category.save()


class Migration(migrations.Migration):
    dependencies = [
        ('projectapp', '0001_initial'),
        ('projectapp', '0002_users'),
    ]

    operations = [
        migrations.RunPython(create_categories_1),
        migrations.RunPython(create_categories_2),
        migrations.RunPython(create_categories_3),
        migrations.RunPython(create_categories_4),
    ]
