# Generated by Django 4.1.2 on 2022-12-05 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_post_videos_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='videos',
            field=models.URLField(blank=True, null=True),
        ),
    ]
