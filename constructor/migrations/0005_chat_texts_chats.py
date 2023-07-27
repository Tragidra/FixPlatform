# Generated by Django 4.2.3 on 2023-07-27 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0004_users_bonus'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat_texts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.IntegerField()),
                ('text', models.TextField()),
                ('autor', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Chats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.IntegerField()),
                ('manager_id', models.IntegerField()),
                ('chat_texts_id', models.IntegerField()),
            ],
        ),
    ]
