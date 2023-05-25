# Generated by Django 4.0.6 on 2023-05-24 09:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_rename_is_centeral_branch_is_central'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='current_fiscal_year',
            field=models.CharField(default='79/80', max_length=20),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='EndDayRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('terminal', models.CharField(max_length=10)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.branch')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
