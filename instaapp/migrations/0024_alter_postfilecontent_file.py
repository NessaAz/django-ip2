# Generated by Django 4.0.5 on 2022-06-23 01:02

from django.db import migrations, models
import instaapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('instaapp', '0023_alter_postfilecontent_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postfilecontent',
            name='file',
            field=models.FileField(upload_to=instaapp.models.user_directory_path),
        ),
    ]
