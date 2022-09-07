# Generated by Django 4.0.1 on 2022-03-17 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0003_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('genre', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('author', models.CharField(max_length=150)),
                ('bookformat', models.CharField(max_length=150)),
                ('isbn', models.CharField(max_length=150)),
                ('pages', models.CharField(max_length=150)),
                ('totalratings', models.CharField(max_length=150)),
                ('image', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=150)),
                ('lastname', models.CharField(max_length=150)),
                ('address', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('password', models.CharField(max_length=150)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
