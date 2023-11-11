# Generated by Django 4.2.7 on 2023-11-09 15:49

import apps.product.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternative_text', models.CharField(max_length=100)),
                ('url', models.ImageField(default='text.jpg', upload_to=None)),
                ('order', apps.product.fields.OrderField(blank=True)),
                ('product_line', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.productline')),
            ],
        ),
    ]