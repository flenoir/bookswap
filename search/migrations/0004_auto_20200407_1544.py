# Generated by Django 2.2.8 on 2020-04-07 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_auto_20200304_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='rental_end',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='rental_start',
            field=models.DateField(null=True),
        ),
    ]
