# Generated by Django 5.1.2 on 2024-12-07 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0004_remove_pedido_data_pedido_remove_pedido_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='chave_pacote',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='metodo_pagamento',
            field=models.CharField(max_length=255),
        ),
    ]