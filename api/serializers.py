from rest_framework import serializers
from core.models import (
    Shop, Client, Staff, FlowerType, Flower,
    Bouquet, BouquetPosition, Orders, OrderPosition,
    FlowerCombination, Storage
)
from django.core.validators import EmailValidator
import re
from datetime import date


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
    
    def validate_email_shop(self, value):
        # DRF уже проверяет формат EmailField, но можно добавить свои правила
        if Shop.objects.filter(email_shop=value).exists():
            raise serializers.ValidationError("Магазин с таким email уже существует.")
        return value

    def validate_inn(self, value):
        s = str(value)
        if not re.fullmatch(r"\d{10}", s):
            raise serializers.ValidationError("ИНН должен содержать ровно 10 цифр.")
        return value

    def validate_ogrnip(self, value):
        s = str(value)
        if not re.fullmatch(r"\d{15}", s):
            raise serializers.ValidationError("ОГРНИП должен содержать 15 цифр.")
        return value

    def validate_number_phone_shop(self, value):
        if not re.fullmatch(r"^(\+7\d{10}|7\d{10})$", value):
            raise serializers.ValidationError(
                "Телефон должен быть в формате +7XXXXXXXXXX или 7XXXXXXXXXX."
            )
        return value


class ClientSerializer(serializers.ModelSerializer):
    # усиливаем проверку формата email
    email_client = serializers.EmailField(max_length=30)

    class Meta:
        model = Client
        fields = "__all__"

    def validate_email_client(self, value):
        qs = Client.objects.filter(email_client=value)
        instance = getattr(self, "instance", None)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "Клиент с таким email уже существует."
            )
        return value

    def validate_phone_number_client(self, value):
        # тот же формат, что и для телефонов сотрудников
        if not re.fullmatch(r"^(\+7\d{10}|7\d{10})$", value):
            raise serializers.ValidationError(
                "Телефон должен быть в формате +7XXXXXXXXXX или 7XXXXXXXXXX."
            )
        return value

    def validate_password_client(self, value):
        # такая же «настоящая» сложность, как для password_staff
        if not 8 <= len(value) <= 20:
            raise serializers.ValidationError(
                "Пароль должен содержать от 8 до 20 символов."
            )
        if not re.search(r"[A-ZА-Я]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну заглавную букву."
            )
        if not re.search(r"[a-zа-я]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну строчную букву."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну цифру."
            )
        if not re.search(r"[!@#$%^&*()_\-]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы один спецсимвол (!@#$%^&*()_-)."
            )
        return value

    def validate_birth_date(self, value):
        if value >= date.today():
            raise serializers.ValidationError(
                "Дата рождения должна быть в прошлом."
            )
        return value


class StaffSerializer(serializers.ModelSerializer):
    email_staff = serializers.EmailField(max_length=30)

    class Meta:
        model = Staff
        fields = "__all__"

    def validate_work_experience_other(self, value):
        
        if value is not None and (value < 0 or value > 1000):
            raise serializers.ValidationError("Стаж должен быть от 0 до 100 лет.")
        return value

    def validate_number_phone_staff(self, value):
    
        if not re.fullmatch(r"^(\+7\d{10}|7\d{10})$", value):
            raise serializers.ValidationError(
                "Телефон должен быть в формате +7XXXXXXXXXX или 7XXXXXXXXXX."
            )
        return value


    def validate_email_staff(self, value):
        qs = Staff.objects.filter(email_staff=value)

    # если это обновление, исключаем текущего сотрудника
        instance = getattr(self, "instance", None)
        if instance is not None:
            qs = qs.exclude(pk=instance.pk)

        if qs.exists():
            raise serializers.ValidationError(
                "Сотрудник с таким email уже существует."
            )
        return value


    def validate_date_employment(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Дата приёма на работу не может быть в будущем."
            )
        return value
    
    def validate_password_staff(self, value):
        # длина
        if not 8 <= len(value) <= 20:
            raise serializers.ValidationError(
                "Пароль должен содержать от 8 до 20 символов."
            )

        # хотя бы одна заглавная буква
        if not re.search(r"[A-ZА-Я]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну заглавную букву."
            )

        # хотя бы одна строчная буква
        if not re.search(r"[a-zа-я]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну строчную букву."
            )

        # хотя бы одна цифра
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы одну цифру."
            )

        # хотя бы один спецсимвол
        if not re.search(r"[!@#$%^&*()_\-]", value):
            raise serializers.ValidationError(
                "Пароль должен содержать хотя бы один спецсимвол (!@#$%^&*()_-)."
            )

        return value    

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
        fields = "__all__"

    def validate_status_order(self, value):
        allowed = ["оформлен", "в обработке", "собран", "завершен"]
        if value not in allowed:
            raise serializers.ValidationError(
                'Статус заказа должен быть одним из: "оформлен", "в обработке", "собран", "завершен".'
            )
        return value

    def validate_payment_type(self, value):
        allowed = ["наличные", "карта"]
        if value not in allowed:
            raise serializers.ValidationError(
                'Способ оплаты должен быть "наличные" или "карта".'
            )
        return value

    def validate_order_date(self, value):
        if value > date.today():
            raise serializers.ValidationError(
                "Дата заказа не может быть в будущем."
            )
        return value


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
