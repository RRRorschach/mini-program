# Generated by Django 3.2.13 on 2022-05-08 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_auto_20220507_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='openId',
            field=models.CharField(max_length=255, null=True),
        ),
    ]