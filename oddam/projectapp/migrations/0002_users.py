from django.db import migrations


def create_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    admin = User.objects.create_superuser(
        username='Admin@admin.com',
        password='StrongAdminPassword1!',
        email='Admin@admin.com'
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.save()


def create_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    user = User.objects.create_user(
        username='Test@user.com',
        password='StrongUserPassword1!',
        email='Test@user.com',
        first_name='Test',
        last_name='Testow',
    )
    user.is_active = True
    user.save()





class Migration(migrations.Migration):
    dependencies = [
        ('projectapp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser),
        migrations.RunPython(create_users),
    ]
