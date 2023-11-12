# Generated by Django 4.2.7 on 2023-11-12 16:18

import apps.product.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, max_length=700)),
            ],
        ),
        migrations.CreateModel(
            name='AttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value', models.CharField(max_length=100)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attribute_values', to='product.attribute')),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=150)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='product.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='name')),
                ('slug', models.SlugField(max_length=150)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('is_digital', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.brand')),
                ('category', mptt.fields.TreeForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product.category')),
            ],
            managers=[
                ('default_manager', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='ProductLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('sku', models.CharField(max_length=100)),
                ('stock_qty', models.IntegerField()),
                ('is_available', models.BooleanField(default=False)),
                ('order', apps.product.fields.OrderField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ProductTypeAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_type_attributes_a', to='product.attribute')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_type_attributes_pt', to='product.producttype')),
            ],
            options={
                'unique_together': {('product_type', 'attribute')},
            },
        ),
        migrations.AddField(
            model_name='producttype',
            name='attributes',
            field=models.ManyToManyField(related_name='product_type_attributes', through='product.ProductTypeAttribute', to='product.attribute'),
        ),
        migrations.CreateModel(
            name='ProductLineAttributeValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attribute_values_av', to='product.attributevalue')),
                ('product_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attribute_values_pl', to='product.productline')),
            ],
            options={
                'unique_together': {('attribute_value', 'product_line')},
            },
        ),
        migrations.AddField(
            model_name='productline',
            name='attribute_values',
            field=models.ManyToManyField(related_name='product_line_attribute_values', through='product.ProductLineAttributeValue', to='product.attributevalue'),
        ),
        migrations.AddField(
            model_name='productline',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='product_lines', to='product.product'),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternative_text', models.CharField(max_length=100)),
                ('url', models.ImageField(upload_to=None)),
                ('order', apps.product.fields.OrderField(blank=True)),
                ('product_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.productline')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_types',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='products', to='product.producttype'),
        ),
    ]
