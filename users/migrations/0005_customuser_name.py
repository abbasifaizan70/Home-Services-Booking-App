# Generated by Django 4.2.7 on 2023-12-19 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='name',
            field=models.CharField(default='Dummay Name', max_length=20),
            preserve_default=False,
        ),
    ]
