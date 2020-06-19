# Generated by Django 3.0.7 on 2020-06-14 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogs', '0005_remove_odercommand_id_oder'),
    ]

    operations = [
        migrations.CreateModel(
            name='CPEAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('edu', models.CharField(max_length=2)),
                ('std', models.CharField(max_length=20)),
                ('cpenumber', models.CharField(max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
