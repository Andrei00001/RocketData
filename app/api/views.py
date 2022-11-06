from django.db import IntegrityError
from django.db.models import Avg
from django.contrib.auth.models import User

from django.http import HttpResponse
from rest_framework import views
from rest_framework.permissions import IsAuthenticated

from app.api import serializer
from app import models
from rest_framework.response import Response

from app.schemas.datetime import ValidDate
from app.tasks import send_email


class ProductsView(views.APIView):
    serializer_class = serializer.ProductsSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        if len(data.get("name")) > 25:
            return HttpResponse("404 product name must not exceed 25 characters")
        try:
            ValidDate.parse_obj({'date': data.get('market_launch_date')})
        except ValueError:
            return HttpResponse(f"404 there is no enterprise with this name {data.get('market_launch_date')}")
        try:
            models.Products.objects.create(name=data.get("name"), model=data.get("model"),
                                           market_launch_date=data.get("market_launch_date"))
        except IntegrityError:
            return HttpResponse(f"404 Such a product already exists {data.get('name')}")

        return HttpResponse("200")


class UpdateProductView(views.APIView):
    serializer_class = serializer.UpdateProductsSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, product_name: str, *args, **kwargs):
        data = request.data
        if len(data.get("new_name")) > 25:
            return HttpResponse("404 product name must not exceed 25 characters")
        try:
            product = models.Products.objects.get(name=product_name)
        except models.Products.DoesNotExist:
            return HttpResponse("404 there is no product with this name")
        try:
            ValidDate.parse_obj({'date': data.get('new_market_launch_date')})
        except ValueError:
            return HttpResponse(f"404 there is no enterprise with this name {data.get('new_market_launch_date')}")

        product.name = data.get("new_name") if data.get(
            "new_name") != product.name and data.get(
            "new_name") != "" and data.get(
            "new_name") != "string" else product.name
        product.model = data.get("new_model") if data.get(
            "new_model") != product.name and data.get(
            "new_model") != "" and data.get(
            "new_model") != "string" else product.model
        product.market_launch_date = data.get("new_market_launch_date")
        product.save()
        return HttpResponse("200")


class DeleteProductsView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, product_name: str, *args, **kwargs):
        try:
            product = models.Products.objects.get(name=product_name)
        except models.Products.DoesNotExist:
            return HttpResponse("404 there is no product with this name")
        product.delete()
        return HttpResponse("200")


class SupplyChainView(views.APIView):
    serializer_class = serializer.SupplyChainViewSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        if len(data.get("provider")) > 50 or len(data.get("recipient")) > 50:
            return HttpResponse("404 provider/recipient name must not exceed 50 characters")
        try:
            provider = models.Enterprise.objects.get(name=data.get("provider"))
            recipient = models.Enterprise.objects.get(name=data.get("recipient"))
        except models.Enterprise.DoesNotExist:
            return HttpResponse("404 there is no enterprise with this name")

        try:
            ValidDate.parse_obj({'date': data.get('move_date')})
        except ValueError:
            return HttpResponse(f"404 there is no enterprise with this name {data.get('move_date')}")
        try:
            models.SupplyChain.objects.create(
                provider=provider,
                recipient=recipient,
                price=data.get("price"),
                move_date=data.get("move_date")
            )
        except IntegrityError:
            return HttpResponse(f"404 This supply chain already exists {data.get('provider')} - {data.get('recipient')}")
        return HttpResponse("200")


class UpdateSupplyChainView(views.APIView):
    serializer_class = serializer.UpdateSupplyChainViewSerializer
    permission_classes = (IsAuthenticated,)

    def put(self, request, provider_name: str, recipient_name: str, *args, **kwargs):
        data = request.data
        if len(data.get("new_provider")) > 50 or len(data.get("new_recipient")) > 50:
            return HttpResponse("404 provider/recipient name must not exceed 50 characters")

        try:
            provider = models.Enterprise.objects.get(name=provider_name)
            recipient = models.Enterprise.objects.get(name=recipient_name)
            supply_chain = models.SupplyChain.objects.get(provider=provider, recipient=recipient)
        except models.Enterprise.DoesNotExist:
            return HttpResponse("404 there is no enterprise with this name or not supply chain")

        except models.SupplyChain.DoesNotExist:
            return HttpResponse("404 there is no enterprise with this name or not supply chain")

        try:
            provider = models.Enterprise.objects.get(name=data.get("new_provider"))
        except models.Enterprise.DoesNotExist:
            return HttpResponse(f"404 there is no enterprise with this name {data.get('new_provider')}")

        try:
            recipient = models.Enterprise.objects.get(name=data.get("new_recipient"))
        except models.Enterprise.DoesNotExist:
            return HttpResponse(f"404 there is no enterprise with this name {data.get('new_recipient')}")

        try:
            ValidDate.parse_obj({'date': data.get('new_move_date')})
        except ValueError:
            return HttpResponse(f"404 there is no enterprise with this name {data.get('new_move_date')}")

        supply_chain.provider = provider
        supply_chain.recipient = recipient
        supply_chain.move_date = data.get('new_move_date')
        try:
            supply_chain.save()
        except Exception:
            return HttpResponse("404 such a network already exists")

        return HttpResponse("200")


class DeleteSupplyChainView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, provider_name: str, recipient_name: str, *args, **kwargs):
        try:
            provider = models.Enterprise.objects.get(name=provider_name)
            recipient = models.Enterprise.objects.get(name=recipient_name)
            supply_chain = models.SupplyChain.objects.get(provider=provider, recipient=recipient)
        except models.Enterprise.DoesNotExist:
            return HttpResponse("404 there is no enterprise with this name or not supply chain")

        except models.SupplyChain.DoesNotExist:
            return HttpResponse("404 there is no enterprise with this name or not supply chain")

        supply_chain.delete()
        return HttpResponse("200")


class EnterpriseView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(get_data_for_enterprise(list(models.Enterprise.objects.filter(user__user=request.user))))


class ListEnterpriseView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response(get_data_for_enterprise(list(models.Enterprise.objects.all())))


class EnterpriseFromCountryView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, country, *args, **kwargs):
        return Response(get_data_for_enterprise(
            list(models.Enterprise.objects.filter(contacts__country=country))))


class StatisticsEnterpriseView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        average_debt = models.SupplyChain.objects.all().aggregate(Avg('price'))['price__avg']
        list_enterprise_statistics = get_data_for_enterprise(
            list(
                models.Enterprise.objects.filter(recipient__price__gt=average_debt)
            )
        )
        if len(list_enterprise_statistics) == 0:
            return HttpResponse("200 There are no enterprises with more than average debt")
        return Response(list_enterprise_statistics)


class ProductsEnterpriseView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, product_id: int, *args, **kwargs):
        return Response(
            get_data_for_enterprise(
                list(models.Enterprise.objects.filter(products__products=product_id).all())
            )
        )


def get_data_for_enterprise(enterprises: list[models.Enterprise]) -> list[list[dict]]:
    list = []
    for enterprise in enterprises:
        enterprise_data = serializer.EmployeesSerializer(
            enterprise
        )
        contacts_data = serializer.EnterpriseContactsSerializer(
            models.EnterpriseContacts.objects.get(enterprise=enterprise)
        )
        products_data = serializer.ProductsSerializer(
            models.Products.objects.filter(enterprise__enterprise=enterprise), many=True
        )
        employees_data = serializer.EnterpriseEmployeesSerializer(
            User.objects.filter(enterprise_user__enterprise=enterprise), many=True
        )
        provider = enterprise.recipient.filter(provider__type__id__lt=enterprise.type.id).last()
        provider_data = serializer.SupplyChainSerializer(provider) if provider else None
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


class QrView(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, name_enterprise: str, *args, **kwargs):
        try:
            contacts = models.EnterpriseContacts.objects.get(enterprise__name=name_enterprise)
        except models.EnterpriseContacts.DoesNotExist:
            return HttpResponse(f"404 company with this name-{name_enterprise} does not exist")

        data = f'email:{contacts.email}\n' \
               f'Address:{contacts.country}-{contacts.city}-{contacts.the_outside}-{contacts.house_number}'
        user_email = request.user.email

        send_email.apply_async(
            args=(
                data,
                name_enterprise,
                user_email,
            ),
            serializer='json',
        )
        return HttpResponse("200")
