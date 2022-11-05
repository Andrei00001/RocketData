from itertools import product

from rest_framework import serializers

from app.models import Products


class ProductsSerializer(serializers.Serializer):
    name = serializers.CharField()
    model = serializers.CharField()
    market_launch_date = serializers.DateField()


class UpdateProductsSerializer(serializers.Serializer):
    new_name = serializers.CharField()
    new_model = serializers.CharField()
    new_market_launch_date = serializers.DateField()


class SupplyChainSerializer(serializers.Serializer):
    provider = serializers.CharField()
    price = serializers.FloatField()
    move_date = serializers.DateTimeField()


class SupplyChainViewSerializer(serializers.Serializer):
    provider = serializers.CharField()
    recipient = serializers.CharField()
    price = serializers.FloatField()
    move_date = serializers.DateTimeField()


class UpdateSupplyChainViewSerializer(serializers.Serializer):
    new_provider = serializers.CharField()
    new_recipient = serializers.CharField()
    new_move_date = serializers.DateTimeField()


class EnterpriseContactsSerializer(serializers.Serializer):
    email = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    the_outside = serializers.CharField()
    house_number = serializers.CharField()


class EnterpriseEmployeesSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.CharField()


class EmployeesSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
