# Generated by Django 4.0.5 on 2022-12-05 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortLinkService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_link', models.CharField(max_length=1000, unique=True)),
                ('short_link', models.CharField(max_length=35, unique=True)),
                ('count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'links',
            },
        ),
    ]