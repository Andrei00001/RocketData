from django.db.models import Avg
from django.http import HttpResponse
from rest_framework import views, filters

from app.api.serializer import EmployeesSerializer, EnterpriseContactsSerializer, ProductsSerializer, \
    EnterpriseEmployeesSerializer, SupplyChainSerializer, SupplyChainViewSerializer, UpdateProductsSerializer, \
    UpdateSupplyChainViewSerializer
from app.models import Enterprise, EnterpriseContacts, SupplyChain, Products
from rest_framework.response import Response


class ProductsView(views.APIView):
    serializer_class = ProductsSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        if len(data.get("name")) > 25:
            return HttpResponse("404 product name must not exceed 25 characters")
        Products.objects.create(name=data.get("name"), model=data.get("model"),
                                market_launch_date=data.get("market_launch_date"))
        return HttpResponse("200")


class UpdateProductView(views.APIView):
    serializer_class = UpdateProductsSerializer

    def put(self, request, product_name: str, *args, **kwargs):
        data = request.data
        if len(data.get("new_name")) > 25:
            return HttpResponse("404 product name must not exceed 25 characters")
        try:
            product = Products.objects.get(name=product_name)
        except Products.DoesNotExist:
            return HttpResponse("404 there is no product with this name")
        product.name = data.get("new_name") if data.get("new_name") != product.name or "" or "string" else product.name
        product.model = data.get("new_model") if data.get(
            "new_model") != product.name or "" or "string" else product.model
        product.market_launch_date = data.get("new_market_launch_date")
        product.save()
        return HttpResponse("200")


class DeleteProductsView(views.APIView):
    def delete(self, request, product_name: str, *args, **kwargs):
        try:
            product = Products.objects.get(name=product_name)
        except Products.DoesNotExist:
            return HttpResponse("404 there is no product with this name")
        product.delete()
        return HttpResponse("200")


class SupplyChainView(views.APIView):
    serializer_class = SupplyChainViewSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        if len(data.get("provider")) > 50 or len(data.get("recipient")) > 50:
            return HttpResponse("404 provider/recipient name must not exceed 50 characters")
        try:
            provider = Enterprise.objects.get(name=data.get("provider"))
            recipient = Enterprise.objects.get(name=data.get("recipient"))
        except Enterprise.DoesNotExist:
            return HttpResponse("404 there is no enterprise with this name")
        SupplyChain.objects.create(
            provider=provider,
            recipient=recipient,
            price=data.get("price"),
            move_date=data.get("move_date")
        )
        return HttpResponse("200")


class UpdateSupplyChainView(views.APIView):
    serializer_class = UpdateSupplyChainViewSerializer

    def put(self, request, provider_name: str, request_name: str, *args, **kwargs):
        data = request.data
        if len(data.get("new_provider")) > 50 or len(data.get("new_recipient")) > 50:
            return HttpResponse("404 provider/recipient name must not exceed 50 characters")
        try:
            provider = Enterprise.objects.get(name=provider_name)
            recipient = Enterprise.objects.get(name=request_name)
            supply_chain = SupplyChain.objects.get(provider=provider, recipient=recipient)
        except Enterprise.DoesNotExist:
            return HttpResponse("404 there is no enterprise with this name or not supply chain")
        try:
            provider = Enterprise.objects.get(name=data.get("new_provider"))
        except Enterprise.DoesNotExist:
            return HttpResponse(f"404 there is no enterprise with this name {data.get('new_provider')}")
        try:
            recipient = Enterprise.objects.get(name=data.get("new_recipient"))
        except Enterprise.DoesNotExist:
            return HttpResponse(f"404 there is no enterprise with this name {data.get('new_recipient')}")
        supply_chain.provider = provider
        supply_chain.recipient = recipient
        supply_chain.move_date = data.get('new_move_date')
        supply_chain.save()
        return HttpResponse("200")


class DeleteSupplyChainView(views.APIView):
    def delete(self, request, provider_name: str, request_name: str, *args, **kwargs):
        try:
            provider = Enterprise.objects.get(name=provider_name)
            recipient = Enterprise.objects.get(name=request_name)
            supply_chain = SupplyChain.objects.get(provider=provider, recipient=recipient)
        except Enterprise.DoesNotExist:
            return HttpResponse("404 there is no enterprise with this name or not supply chain")
        supply_chain.delete()
        return HttpResponse("200")


class EnterpriseView(views.APIView):
    def get(self, request, *args, **kwargs):
        return Response(get_data_for_enterprise(list(Enterprise.objects.all())))


class EnterpriseFromCountryView(views.APIView):
    def get(self, request, country, *args, **kwargs):
        return Response(get_data_for_enterprise(list(Enterprise.objects.filter(contacts__country=country).all())))


class StatisticsEnterpriseView(views.APIView):
    def get(self, request, *args, **kwargs):
        average_debt = SupplyChain.objects.all().aggregate(Avg('price'))['price__avg']
        return Response(
            get_data_for_enterprise(list(Enterprise.objects.filter(recipient__price__gt=average_debt).all())))


class ProductsEnterpriseView(views.APIView):
    def get(self, request, product_id: int, *args, **kwargs):
        return Response(
            get_data_for_enterprise(list(Enterprise.objects.filter(products__products=product_id).all())))


def get_data_for_enterprise(enterprises: list[Enterprise]) -> list[list[dict]]:
    list = []
    for enterprise in enterprises:
        enterprise_data = EmployeesSerializer(enterprise)
        contacts_data = EnterpriseContactsSerializer(EnterpriseContacts.objects.get(enterprise=enterprise))
        products_data = ProductsSerializer(Products.objects.filter(enterprise__enterprise=enterprise),
                                           many=True)
        employees_data = EnterpriseEmployeesSerializer(enterprise.employees.all(), many=True)
        provider = enterprise.recipient.filter(provider__type__id__lt=enterprise.type.id).last()
        provider_data = SupplyChainSerializer(provider) if provider else None
        list.append(
            [
                {'enterprise': enterprise_data.data},
                {'contacts': contacts_data.data},
                {'products': products_data.data},
                {'employees': employees_data.data},
                {'debt': provider_data.data if provider_data else None}
            ]
        )

    return list
