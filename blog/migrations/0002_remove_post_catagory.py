# Generated by Django 4.1 on 2022-09-15 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='catagory',
        ),
    ]
