# Generated by Django 3.2.5 on 2023-04-18 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apipoint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='paystackmodel',
            name='bank',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
