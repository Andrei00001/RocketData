# Generated by Django 4.1.3 on 2022-11-04 13:51
import datetime

from django.conf import settings
from django.db import migrations, models


def create(apps, schema_editor):
    EnterpriseProducts = apps.get_model('app', 'EnterpriseProducts')
    SupplyChain = apps.get_model('app', 'SupplyChain')
    SupplyChainProducts = apps.get_model('app', 'SupplyChainProducts')

    list_supply_chain_products = [
        [1, 2, ],
        [2, 4, ],
    ]
    list_query = []
    for value in list_supply_chain_products:
        supply_chain = SupplyChain.objects.get(pk=value[0])
        product = EnterpriseProducts.objects.get(pk=value[1])
        list_query.append(
            SupplyChainProducts(
                supply_chain=supply_chain,
                products=product,
            )
        )
    SupplyChainProducts.objects.bulk_create(list_query)


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0007_create_supply_chain"),
    ]

    operations = [
        migrations.RunPython(create),
    ]
