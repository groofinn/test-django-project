# Generated by Django 3.1 on 2020-11-29 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0009_auto_20201129_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='first_auth_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
