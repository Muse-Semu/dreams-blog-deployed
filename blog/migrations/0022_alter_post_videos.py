# Generated by Django 4.1.2 on 2022-12-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_alter_post_videos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='videos',
            field=models.FileField(blank=True, null=True, upload_to='image'),
        ),
    ]
