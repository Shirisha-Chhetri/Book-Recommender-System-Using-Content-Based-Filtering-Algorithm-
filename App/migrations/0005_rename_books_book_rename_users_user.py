# Generated by Django 4.0.1 on 2022-03-17 03:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_books_users_delete_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Books',
            new_name='Book',
        ),
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]