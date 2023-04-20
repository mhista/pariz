# Generated by Django 3.2.5 on 2023-03-09 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userMgt', '0006_remove_address_suite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_choice',
            field=models.CharField(choices=[('B', 'Billing'), ('S', 'Shipping')], max_length=1),
        ),
        migrations.AlterField(
            model_name='address',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
