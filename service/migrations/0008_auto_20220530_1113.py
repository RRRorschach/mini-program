# Generated by Django 3.2.13 on 2022-05-30 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_signinforstudent_signinforteacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='endTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='signinforstudent',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='signinforstudent',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='signinforstudent',
            name='time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='signinforteacher',
            name='endTime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='signinforteacher',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='signinforteacher',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='signinforteacher',
            name='startTime',
            field=models.DateTimeField(null=True),
        ),
    ]