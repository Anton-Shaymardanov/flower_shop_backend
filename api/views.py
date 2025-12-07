from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection

from core.models import (
    Shop, Client, Staff, FlowerType, Flower,
    Bouquet, BouquetPosition, Orders, OrderPosition,
    FlowerCombination, Storage
)
from .serializers import (
    ShopSerializer, ClientSerializer, StaffSerializer,
    FlowerTypeSerializer, FlowerSerializer,
    BouquetSerializer, BouquetPositionSerializer,
    OrdersSerializer, OrderPositionSerializer,
    FlowerCombinationSerializer, StorageSerializer
)



class ShopListCreateView(generics.ListCreateAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class ShopRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer




class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer




class StaffListCreateView(generics.ListCreateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffByPositionView(generics.ListAPIView):
    serializer_class = StaffSerializer

    def get_queryset(self):
        position = self.kwargs['position']
        return Staff.objects.filter(position=position)




class FlowerTypeListCreateView(generics.ListCreateAPIView):
    queryset = FlowerType.objects.all()
    serializer_class = FlowerTypeSerializer


class FlowerTypeRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FlowerType.objects.all()
    serializer_class = FlowerTypeSerializer


class FlowerListCreateView(generics.ListCreateAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer


class FlowerRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Flower.objects.all()
    serializer_class = FlowerSerializer




class BouquetListCreateView(generics.ListCreateAPIView):
    queryset = Bouquet.objects.all()
    serializer_class = BouquetSerializer


class BouquetRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bouquet.objects.all()
    serializer_class = BouquetSerializer


class BouquetPositionListCreateView(generics.ListCreateAPIView):
    queryset = BouquetPosition.objects.all()
    serializer_class = BouquetPositionSerializer


class BouquetPositionRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BouquetPosition.objects.all()
    serializer_class = BouquetPositionSerializer


class BouquetPositionsByBouquetView(generics.ListAPIView):
    serializer_class = BouquetPositionSerializer

    def get_queryset(self):
        bouquet_id = self.kwargs['bouquet_id']
        return BouquetPosition.objects.filter(id_bouquet=bouquet_id)




class OrdersListCreateView(generics.ListCreateAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrdersRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer


class OrderPositionListCreateView(generics.ListCreateAPIView):
    queryset = OrderPosition.objects.all()
    serializer_class = OrderPositionSerializer


class OrderPositionRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderPosition.objects.all()
    serializer_class = OrderPositionSerializer


class OrderPositionsByOrderView(generics.ListAPIView):
    serializer_class = OrderPositionSerializer

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return OrderPosition.objects.filter(id_order=order_id)




class FlowerCombinationListCreateView(generics.ListCreateAPIView):
    queryset = FlowerCombination.objects.all()
    serializer_class = FlowerCombinationSerializer


class FlowerCombinationRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FlowerCombination.objects.all()
    serializer_class = FlowerCombinationSerializer


class StorageListCreateView(generics.ListCreateAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer


class StorageRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer




class ProcedureAPIView(APIView):
    # POST /api/procedures/sp_insert_client/
    def post(self, request, proc_name):
        params = list(request.data.values())

        try:
            placeholders = ", ".join(["%s"] * len(params))
            sql = f"CALL {proc_name}({placeholders})"

            with connection.cursor() as cursor:
                cursor.execute(sql, params)

            return Response(
                {"status": "ok", "procedure": proc_name},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            print("PROC ERROR:", repr(e))
            return Response(
                {"status": "error", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class FunctionAPIView(APIView):
    
    def get(self, request, func_name):
       
        params = list(request.GET.values())

        try:
            with connection.cursor() as cursor:
                
                cursor.callproc(func_name, params)

                cols = [col[0] for col in cursor.description] if cursor.description else []
                rows = cursor.fetchall() if cursor.description else []

            data = [dict(zip(cols, row)) for row in rows]
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"status": "error", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
