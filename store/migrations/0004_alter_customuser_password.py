# Generated by Django 5.1.6 on 2025-03-09 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_customuser_options_customuser_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
