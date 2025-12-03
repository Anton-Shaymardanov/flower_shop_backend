from rest_framework import serializers
from core.models import (
    Shop, Client, Staff, FlowerType, Flower,
    Bouquet, BouquetPosition, Orders, OrderPosition,
    FlowerCombination, Storage
)


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class FlowerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowerType
        fields = '__all__'


class FlowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flower
        fields = '__all__'


class BouquetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bouquet
        fields = '__all__'


class BouquetPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BouquetPosition
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class OrderPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderPosition
        fields = '__all__'


class FlowerCombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlowerCombination
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'
