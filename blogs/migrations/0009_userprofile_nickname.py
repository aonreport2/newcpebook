# Generated by Django 3.0.7 on 2020-06-15 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0008_auto_20200615_0547'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
