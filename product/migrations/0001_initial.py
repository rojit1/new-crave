# Generated by Django 4.0.6 on 2023-05-18 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductMultiprice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.BigIntegerField()),
                ('product_price', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'product_multiprice',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BranchStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('quantity', models.PositiveIntegerField()),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BranchStockTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('opening', models.IntegerField(default=0)),
                ('received', models.IntegerField(default=0)),
                ('wastage', models.IntegerField(default=0)),
                ('returned', models.IntegerField(default=0)),
                ('sold', models.IntegerField(default=0)),
                ('closing', models.IntegerField(default=0)),
                ('physical', models.IntegerField(default=0)),
                ('discrepancy', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CustomerProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('price', models.FloatField(default=0.0)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=255, unique=True, verbose_name='Item Name')),
                ('slug', models.SlugField(verbose_name='Item Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Item Description')),
                ('unit', models.CharField(blank=True, max_length=100, null=True)),
                ('is_taxable', models.BooleanField(default=True)),
                ('price', models.FloatField(default=0.0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/images/')),
                ('group', models.CharField(max_length=20)),
                ('product_id', models.CharField(blank=True, max_length=255, null=True)),
                ('barcode', models.CharField(blank=True, max_length=100, null=True)),
                ('is_produced', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('title', models.CharField(choices=[('FOOD', 'FOOD'), ('BEVERAGE', 'BEVERAGE'), ('OTHERS', 'OTHERS')], default='FOOD', max_length=255, unique=True, verbose_name='Product Type')),
                ('slug', models.SlugField(unique=True, verbose_name='Category Slug')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('stock_quantity', models.PositiveSmallIntegerField(default=0)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.productcategory'),
        ),
        migrations.CreateModel(
            name='ItemReconcilationApiItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('sorting_order', models.IntegerField(default=0)),
                ('is_featured', models.BooleanField(default=False)),
                ('date', models.DateField(blank=True, null=True)),
                ('wastage', models.IntegerField(default=0)),
                ('returned', models.IntegerField(default=0)),
                ('physical', models.IntegerField(default=0)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organization.branch')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='product.product')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]
