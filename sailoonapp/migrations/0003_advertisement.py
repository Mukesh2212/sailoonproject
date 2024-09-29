# Generated by Django 5.1 on 2024-08-14 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sailoonapp', '0002_businesslisting_distance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('end_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('start_date', models.DateField(auto_created=True, blank=True, null=True)),
                ('age', models.CharField(blank=True, max_length=200, null=True)),
                ('range', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('target_audience', models.CharField(blank=True, choices=[('age', 'age'), ('range', 'range'), ('location', 'location')], max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]