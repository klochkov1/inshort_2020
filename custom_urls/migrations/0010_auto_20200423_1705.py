# Generated by Django 3.0.5 on 2020-04-23 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_urls', '0009_auto_20200423_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='custom_url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_urls.CustomUrl'),
        ),
    ]
