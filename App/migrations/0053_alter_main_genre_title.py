# Generated by Django 4.0.1 on 2022-07-08 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0052_remove_genre_main_category_genre_main_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_genre',
            name='title',
            field=models.CharField(max_length=50, null=b'I01\n'),
        ),
    ]