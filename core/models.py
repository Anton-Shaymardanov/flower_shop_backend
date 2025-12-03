from django.db import models




class Shop(models.Model):
    id_shop = models.AutoField(primary_key=True)
    email_shop = models.CharField(max_length=30, unique=True)
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
    email_client = models.CharField(max_length=30)

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
    email_staff = models.CharField(max_length=30)

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
    price = models.DecimalField(max_digits=5, decimal_places=2)

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


class FlowerCombination(models.Model):
    id_combination = models.AutoField(primary_key=True)
    id_flower_type_1 = models.IntegerField()
    id_flower_type_2 = models.IntegerField()
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
