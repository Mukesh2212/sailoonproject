# Generated by Django 5.1.4 on 2025-01-30 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sailoonapp', '0005_alter_user_deactivated_at_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('contact', models.CharField(blank=True, max_length=13, null=True)),
            ],
        ),
    ]
