# Generated by Django 4.0.6 on 2023-03-15 04:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_alter_printersettings_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PrinterSettings',
            new_name='PrinterSetting',
        ),
    ]
