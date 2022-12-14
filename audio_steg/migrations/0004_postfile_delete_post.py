# Generated by Django 4.1.3 on 2022-11-05 09:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('audio_steg', '0003_auto_20190418_1911'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=255)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('file_hidden', models.TextField(max_length=255)),
                ('state', models.CharField(max_length=15)),
                ('type_file_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
