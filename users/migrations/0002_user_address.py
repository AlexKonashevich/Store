# Generated by Django 4.2.2 on 2023-09-13 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default=0, max_length=264),
            preserve_default=False,
        ),
    ]