# Generated by Django 4.2.3 on 2023-07-27 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0002_alter_users_passport'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='referral_id',
            field=models.IntegerField(null=True),
        ),
    ]
