# Generated by Django 3.2.5 on 2023-03-07 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userMgt', '0005_rename_adrress_choice_address_address_choice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='suite',
        ),
    ]
