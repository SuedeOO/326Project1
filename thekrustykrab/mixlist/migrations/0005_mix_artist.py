# Generated by Django 2.0.2 on 2018-03-27 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mixlist', '0004_auto_20180327_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='mix',
            name='artist',
            field=models.CharField(max_length=80, null=True),
        ),
    ]
