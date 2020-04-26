# Generated by Django 3.0.5 on 2020-04-26 13:20

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sessions', '0001_initial'),
        ('custom_urls', '0011_auto_20200423_1727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customurl',
            old_name='destination_url',
            new_name='source_url',
        ),
        migrations.RemoveField(
            model_name='customurl',
            name='id',
        ),
        migrations.AddField(
            model_name='customurl',
            name='session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sessions.Session'),
        ),
        migrations.AlterField(
            model_name='customurl',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 26, 13, 20, 18, 581520, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='customurl',
            name='short_url',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='visit',
            name='custom_url',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_urls.CustomUrl'),
        ),
    ]
