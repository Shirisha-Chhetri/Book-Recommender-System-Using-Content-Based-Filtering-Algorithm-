# Generated by Django 4.0.1 on 2022-07-08 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0050_alter_genre_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_genre',
            name='title',
            field=models.CharField(max_length=50, null=b'I01\n'),
        ),
    ]
