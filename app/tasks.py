import random

from django.db import transaction

from RocketData.celery import celery_app
from app.models import SupplyChain, Enterprise


@celery_app.task
def sync_bods():
    supply_chains = SupplyChain.objects.filter(price__gt=0)
    for supply_chain in supply_chains:
        with transaction.atomic():
            supply_chain.price += random.uniform(5, 500)
            supply_chain.save()


@celery_app.task
def sync_bods2():
    supply_chains = SupplyChain.objects.filter(price__gt=0)
    for supply_chain in supply_chains:
        with transaction.atomic():
            supply_chain.price -= random.uniform(100, 10_000)
            supply_chain.save()\

@celery_app.task
def sync_bods3(queryset: list[id]):
    if not isinstance(queryset, list):
        queryset = [queryset]
    queryset = Enterprise.objects.filter(pk__in=queryset)
    for enterprise in queryset:
        enterprise = enterprise.recipient.last()
        enterprise.price = 0
        enterprise.save()
