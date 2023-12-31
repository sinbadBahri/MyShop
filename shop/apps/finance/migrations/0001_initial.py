# Generated by Django 4.2.7 on 2023-11-29 15:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='gateway title')),
                ('gateway_request_url', models.CharField(blank=True, max_length=100, null=True, verbose_name='request url')),
                ('gateway_verify_url', models.CharField(blank=True, max_length=100, null=True, verbose_name='verify url')),
                ('gateway_code', models.CharField(choices=[('zarrinpal', 'Zarrinpal'), ('saman', 'Saman'), ('parsian', 'Parsian'), ('shaparak', 'Shaparak'), ('idpay', 'Idpay')], max_length=12, verbose_name='gateway code')),
                ('is_enable', models.BooleanField(default=True, verbose_name='is enable')),
                ('auth_data', models.TextField(blank=True, null=True, verbose_name='auth data')),
            ],
            options={
                'verbose_name': 'Gateway',
                'verbose_name_plural': 'Gateways',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='invoice number')),
                ('amount', models.PositiveIntegerField(verbose_name='payment amount')),
                ('is_paid', models.BooleanField(default=False, verbose_name='is paid status')),
                ('payment_log', models.TextField(blank=True, verbose_name='logs')),
                ('authority', models.CharField(blank=True, max_length=64, verbose_name='authority')),
                ('gateway', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='finance.gateway', verbose_name='gateway')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
