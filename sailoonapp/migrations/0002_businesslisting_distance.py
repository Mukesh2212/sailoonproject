# Generated by Django 5.1 on 2024-08-13 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sailoonapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesslisting',
            name='distance',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]