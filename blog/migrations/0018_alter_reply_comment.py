# Generated by Django 4.1 on 2022-10-06 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_rename_replycomment_reply'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='blog.comment'),
        ),
    ]
