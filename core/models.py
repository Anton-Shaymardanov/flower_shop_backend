from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class Shop(models.Model):
    id_shop = models.AutoField(primary_key=True)
    email_shop = models.EmailField(
        max_length=30,
        unique=True,
        validators=[EmailValidator(message="Введите корректный email.")]
    )
    full_name_shop = models.CharField(max_length=50)
    inn = models.DecimalField(max_digits=10, decimal_places=0)
    number_phone_shop = models.CharField(max_length=12)
    store_address = models.CharField(max_length=50)
    ogrnip = models.DecimalField(max_digits=15, decimal_places=0)

    class Meta:
        db_table = 'shop'
        managed = False


class Client(models.Model):
    id_client = models.AutoField(primary_key=True)
    last_name_client = models.CharField(max_length=20)
    first_name_client = models.CharField(max_length=20)
    middle_name_client = models.CharField(max_length=20)
    phone_number_client = models.CharField(max_length=12)
    password_client = models.CharField(max_length=20)
    birth_date = models.DateField()
    email_client = models.EmailField(
        max_length=30,
        unique=True,
        validators=[EmailValidator(message="Введите корректный email клиента.")]
    )

    class Meta:
        db_table = 'client'
        managed = False


class Staff(models.Model):
    id_staff = models.AutoField(primary_key=True)
    id_shop = models.IntegerField()
    password_staff = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    work_experience_other = models.DecimalField(max_digits=3, decimal_places=0, null=True, blank=True)
    date_employment = models.DateField()
    number_phone_staff = models.CharField(max_length=12)
    first_name_staff = models.CharField(max_length=20)
    last_name_staff = models.CharField(max_length=20)
    email_staff = models.EmailField(
        max_length=30,
        validators=[EmailValidator(message="Введите корректный email сотрудника.")]
    )

    class Meta:
        db_table = 'staff'
        managed = False


class FlowerType(models.Model):
    id_flower_type = models.AutoField(primary_key=True)
    name_flower_type = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'flower_type'
        managed = False


class Flower(models.Model):
    id_flower = models.AutoField(primary_key=True)
    name_flower = models.CharField(max_length=20, unique=True)
    id_flower_type = models.IntegerField()
    price_flower = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'flower'
        managed = False


class Bouquet(models.Model):
    id_bouquet = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        db_table = 'bouquet'
        managed = False





class BouquetPosition(models.Model):
    id_bouquet_position = models.AutoField(primary_key=True)
    id_bouquet = models.IntegerField()
    id_flower = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'bouquet_position'
        managed = False

    def clean(self):
        from .models import Flower, FlowerCombination, BouquetPosition

        # тип добавляемого цветка
        new_flower = Flower.objects.get(id_flower=self.id_flower)
        new_type = new_flower.id_flower_type

        # уже существующие позиции этого букета (кроме текущей при обновлении)
        existing_positions = BouquetPosition.objects.filter(
            id_bouquet=self.id_bouquet
        ).exclude(pk=self.pk)

        for pos in existing_positions:
            other_flower = Flower.objects.get(id_flower=pos.id_flower)
            other_type = other_flower.id_flower_type

            # упорядочиваем типы, чтобы совпало с таблицей flower_combination
            t1, t2 = sorted([new_type, other_type])

            comb = FlowerCombination.objects.filter(
                id_flower_type1=t1,
                id_flower_type2=t2
            ).first()

            # если записи нет или статус False — запрещаем
            if not comb or comb.compatibility_status is False:
                raise ValidationError(
                    "Этот цветок несовместим с уже добавленными в букет."
                )

    def recalculate_bouquet_price(self):
        from .models import Flower, Bouquet, BouquetPosition

        positions = BouquetPosition.objects.filter(id_bouquet=self.id_bouquet)

        total = 0
        for pos in positions:
            flower_price = Flower.objects.get(id_flower=pos.id_flower).price_flower
            total += pos.quantity * flower_price

        bouquet = Bouquet.objects.get(id_bouquet=self.id_bouquet)
        bouquet.price = total
        bouquet.save(update_fields=["price"])

    def save(self, *args, **kwargs):
        # сначала проверка совместимости
        self.clean()
        super().save(*args, **kwargs)
        self.recalculate_bouquet_price()

    def delete(self, *args, **kwargs):
        bouquet_id = self.id_bouquet
        super().delete(*args, **kwargs)
        from .models import BouquetPosition, Bouquet

        if BouquetPosition.objects.filter(id_bouquet=bouquet_id).exists():
            self.recalculate_bouquet_price()
        else:
            bouquet = Bouquet.objects.get(id_bouquet=bouquet_id)
            bouquet.price = 0
            bouquet.save(update_fields=["price"])


class Orders(models.Model):
    id_order = models.AutoField(primary_key=True)
    id_client = models.IntegerField()
    id_shop = models.IntegerField()
    id_staff = models.IntegerField()
    total_amount = models.DecimalField(max_digits=5, decimal_places=2)
    status_order = models.CharField(max_length=15)
    payment_type = models.CharField(max_length=15)
    order_date = models.DateField()

    class Meta:
        db_table = 'orders'
        managed = False


class OrderPosition(models.Model):
    id_order_position = models.AutoField(primary_key=True)
    id_bouquet = models.IntegerField()
    id_order = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_position'
        managed = False

    def recalculate_order_total(self):
        from .models import Orders, OrderPosition, Bouquet

        positions = OrderPosition.objects.filter(id_order=self.id_order)
        total = 0
        for pos in positions:
            bouquet_price = Bouquet.objects.get(id_bouquet=pos.id_bouquet).price
            total += pos.quantity * bouquet_price

        order = Orders.objects.get(id_order=self.id_order)
        order.total_amount = total
        order.save(update_fields=["total_amount"])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.recalculate_order_total()

    def delete(self, *args, **kwargs):
        order_id = self.id_order
        super().delete(*args, **kwargs)
        from .models import OrderPosition, Orders
        if OrderPosition.objects.filter(id_order=order_id).exists():
            self.recalculate_order_total()
        else:
            order = Orders.objects.get(id_order=order_id)
            order.total_amount = 0
            order.save(update_fields=["total_amount"])


class FlowerCombination(models.Model):
    id_combination = models.AutoField(primary_key=True)
    id_flower_type1 = models.IntegerField()
    id_flower_type2 = models.IntegerField()
    compatibility_status = models.BooleanField()

    class Meta:
        db_table = 'flower_combination'
        managed = False


class Storage(models.Model):
    id_storage_item = models.AutoField(primary_key=True)
    id_flower = models.IntegerField()
    quantity_flower = models.IntegerField()
    expiry_date = models.DateField()

    class Meta:
        db_table = 'storage'
        managed = False

