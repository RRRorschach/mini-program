# Generated by Django 3.2.13 on 2022-05-28 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0003_alter_user_openid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseId', models.CharField(max_length=255, null=True)),
                ('courseName', models.CharField(max_length=255, null=True)),
                ('endTime', models.DateTimeField()),
                ('state', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='CourseForTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseId', models.CharField(max_length=255, null=True)),
                ('number', models.CharField(max_length=255, null=True)),
            ],
        ),
    ]
