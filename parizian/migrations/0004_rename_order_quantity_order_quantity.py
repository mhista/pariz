# Generated by Django 3.2.5 on 2023-03-02 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('parizian', '0003_order_order_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_quantity',
            new_name='quantity',
        ),
    ]
