# Generated by Django 4.0.6 on 2023-04-16 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_profile_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='image',
            field=models.CharField(default='empty', max_length=50),
        ),
    ]
