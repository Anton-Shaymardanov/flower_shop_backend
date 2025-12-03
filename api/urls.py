from django.urls import path
from . import views

urlpatterns = [
    # Shops
    path('shops/', views.ShopListCreateView.as_view()),
    path('shops/<int:pk>/', views.ShopRUDView.as_view()),

    # Clients
    path('clients/', views.ClientListCreateView.as_view()),
    path('clients/<int:pk>/', views.ClientRUDView.as_view()),

    # Staff
    path('staff/', views.StaffListCreateView.as_view()),
    path('staff/<int:pk>/', views.StaffRUDView.as_view()),
    path('staff/position/<str:position>/', views.StaffByPositionView.as_view()),

    # FlowerType / Flower
    path('flower-types/', views.FlowerTypeListCreateView.as_view()),
    path('flower-types/<int:pk>/', views.FlowerTypeRUDView.as_view()),
    path('flowers/', views.FlowerListCreateView.as_view()),
    path('flowers/<int:pk>/', views.FlowerRUDView.as_view()),

    # Bouquet / BouquetPosition
    path('bouquets/', views.BouquetListCreateView.as_view()),
    path('bouquets/<int:pk>/', views.BouquetRUDView.as_view()),
    path('bouquet-positions/', views.BouquetPositionListCreateView.as_view()),
    path('bouquet-positions/<int:pk>/', views.BouquetPositionRUDView.as_view()),
    path('bouquets/<int:bouquet_id>/positions/', views.BouquetPositionsByBouquetView.as_view()),

    # Orders / OrderPositions
    path('orders/', views.OrdersListCreateView.as_view()),
    path('orders/<int:pk>/', views.OrdersRUDView.as_view()),
    path('orders/<int:order_id>/positions/', views.OrderPositionsByOrderView.as_view()),
    path('order-positions/', views.OrderPositionListCreateView.as_view()),
    path('order-positions/<int:pk>/', views.OrderPositionRUDView.as_view()),

    # FlowerCombination / Storage
    path('flower-combinations/', views.FlowerCombinationListCreateView.as_view()),
    path('flower-combinations/<int:pk>/', views.FlowerCombinationRUDView.as_view()),
    path('storage/', views.StorageListCreateView.as_view()),
    path('storage/<int:pk>/', views.StorageRUDView.as_view()),

    # Procedures & Functions
    path('procedures/<str:proc_name>/', views.ProcedureAPIView.as_view()),
    path('functions/<str:func_name>/', views.FunctionAPIView.as_view()),
]
