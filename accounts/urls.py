from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("menu/", views.menu_view, name="menu"),
    path("flowers/", views.flowers_list_view, name="flowers"),
    path("flowers/<int:bouquet_id>/", views.flower_detail_view, name="flower_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:bouquet_id>/", views.cart_add_view, name="cart_add"),
    path("cart/clear/", views.cart_clear_view, name="cart_clear"),
    path("cart/checkout/", views.cart_checkout_view, name="cart_checkout"),
    path("my-orders/", views.my_orders_view, name="my_orders"),
    path("staff/orders/free/", views.staff_free_orders_view, name="staff_free_orders"),
    path("staff/orders/take/<int:order_id>/", views.staff_take_order_view, name="staff_take_order"),
    path("staff/orders/mine/", views.staff_my_orders_view, name="staff_my_orders"),
    path("staff/orders/update-status/<int:order_id>/", views.staff_update_order_status_view, name="staff_update_order_status"),
]
