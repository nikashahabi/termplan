# Generated by Django 2.2.10 on 2020-04-11 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0006_auto_20200411_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='semestercourse',
            name='info',
            field=models.TextField(blank=True, null=True),
        ),
    ]
