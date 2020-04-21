# Generated by Django 3.0.5 on 2020-04-21 11:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_urls', '0005_auto_20200421_0020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('visitor_ip', models.GenericIPAddressField(null=True)),
                ('visitor_location', models.CharField(max_length=200, null=True)),
                ('custom_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='custom_urls.CustomUrl')),
            ],
            options={
                'ordering': ['custom_url__owner', 'datetime'],
            },
        ),
        migrations.DeleteModel(
            name='VisitsHistory',
        ),
    ]
