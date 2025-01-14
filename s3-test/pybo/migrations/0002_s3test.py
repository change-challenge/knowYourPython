# Generated by Django 5.1.4 on 2025-01-14 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pybo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='S3TEST',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file_path', models.CharField(max_length=200)),
                ('dt_created', models.DateTimeField(auto_now_add=True)),
                ('dt_modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
