# Generated by Django 5.1.6 on 2025-03-02 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_customer_options_customer_customer_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='customer_code',
            new_name='code',
        ),
    ]
