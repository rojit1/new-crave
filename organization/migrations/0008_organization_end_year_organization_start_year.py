# Generated by Django 4.0.6 on 2023-05-10 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_alter_printersetting_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='end_year',
            field=models.IntegerField(default=2078),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='start_year',
            field=models.IntegerField(default=2079),
            preserve_default=False,
        ),
    ]
