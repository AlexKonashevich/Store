# Generated by Django 4.2.2 on 2023-07-16 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_verified_emailverification'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverification',
            name='expiration',
            field=models.DateTimeField(default=None),
        ),
    ]