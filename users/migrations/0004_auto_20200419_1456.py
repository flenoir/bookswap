# Generated by Django 2.2.8 on 2020-04-19 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200408_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrowing',
            name='borrowing_user',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='borrowing',
            name='rental_validation',
            field=models.BooleanField(default=False),
        ),
    ]
