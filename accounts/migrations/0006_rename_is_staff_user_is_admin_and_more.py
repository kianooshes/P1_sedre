# Generated by Django 5.0.4 on 2024-05-08 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_managers_rename_is_admin_user_is_staff_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_staff',
            new_name='is_admin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_superuser',
        ),
    ]