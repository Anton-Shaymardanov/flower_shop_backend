from django.contrib import admin
from .models import (
    Shop, Client, Staff, FlowerType, Flower,
    Bouquet, BouquetPosition, Orders, OrderPosition,
    FlowerCombination, Storage
)

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id_shop', 'full_name_shop', 'email_shop')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id_client', 'last_name_client', 'first_name_client', 'email_client')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id_staff', 'first_name_staff', 'last_name_staff', 'position')


admin.site.register(FlowerType)
admin.site.register(Flower)
admin.site.register(Bouquet)
admin.site.register(BouquetPosition)
admin.site.register(Orders)
admin.site.register(OrderPosition)
admin.site.register(FlowerCombination)
admin.site.register(Storage)
