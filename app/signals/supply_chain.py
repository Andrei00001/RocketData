from django.db.models.signals import post_save
from django.dispatch import receiver

from app.models import SupplyChain, EnterpriseProducts, SupplyChainProducts


@receiver(post_save, sender=SupplyChainProducts)
def supply_chain_product(**kwargs):
    instance = kwargs['instance']
    created = kwargs['created']

    if created:
        recipient = SupplyChain.objects.get(products_supply_chain=instance).recipient
        product = instance.products.products
        EnterpriseProducts.objects.create(
            enterprise=recipient,
            products=product
        )
