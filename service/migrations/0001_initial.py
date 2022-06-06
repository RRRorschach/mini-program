# Generated by Django 3.2.13 on 2022-05-07 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_id', models.CharField(max_length=255)),
                ('identity', models.BigIntegerField(null=True)),
                ('name', models.CharField(max_length=255, null=True)),
                ('number', models.CharField(max_length=255, null=True)),
                ('face_url', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
