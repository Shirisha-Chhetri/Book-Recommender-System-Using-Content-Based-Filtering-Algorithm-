# Generated by Django 4.0.1 on 2022-07-09 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0063_category_genre_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='category',
        ),
        migrations.AddField(
            model_name='genre',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='App.category'),
            preserve_default=False,
        ),
    ]
