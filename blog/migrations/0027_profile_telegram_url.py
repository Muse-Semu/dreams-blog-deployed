# Generated by Django 4.1.2 on 2023-01-14 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_profile_facebook_url_profile_instagram_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='telegram_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]