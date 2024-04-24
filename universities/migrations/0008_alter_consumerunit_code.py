# Generated by Django 4.1 on 2024-03-28 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('universities', '0007_university_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumerunit',
            name='code',
            field=models.CharField(help_text='Cheque a conta de luz para obter o código da Unidade Consumidora. Insira apenas números', max_length=30, unique=True, verbose_name='Código da Unidade Consumidora'),
        ),
    ]