# Generated by Django 5.1.2 on 2024-12-07 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produtos', '0003_pedido'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='data_pedido',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='status',
        ),
        migrations.AlterField(
            model_name='pedido',
            name='carrinho',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.carrinho'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='chave_pacote',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='endereco_entrega',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='metodo_pagamento',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='nome_destinatario',
            field=models.CharField(max_length=255),
        ),
    ]