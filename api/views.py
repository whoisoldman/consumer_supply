from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    WarehouseSerializer,
    ProductSerializer,
    StockSerializer
)
from .permissions import IsSupplier, IsConsumer
from .models import Warehouse, Product, Stock
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": serializer.data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key
        }, status=status.HTTP_200_OK)

class WarehouseListCreateView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, IsSupplier]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WarehouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated, IsSupplier]

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSupplier]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsSupplier]

class StockListView(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'supplier':
            return Stock.objects.filter(warehouse__owner=user)
        elif user.user_type == 'consumer':
            return Stock.objects.all()
        return Stock.objects.none()

class StockDetailView(generics.RetrieveAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

class SupplyProductView(generics.CreateAPIView):
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, IsSupplier]

    def create(self, request, *args, **kwargs):
        data = request.data
        warehouse_id = data.get('warehouse')
        product_id = data.get('product')
        quantity = data.get('quantity', 0)

        # Проверка, что склад принадлежит текущему поставщику
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id, owner=request.user)
        except Warehouse.DoesNotExist:
            return Response({"error": "Склад не найден или вы не являетесь его владельцем."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что товар существует
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что количество положительное
        if quantity <= 0:
            return Response({"error": "Количество должно быть положительным."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Получение или создание записи в Stock
        stock, created = Stock.objects.get_or_create(warehouse=warehouse, product=product)
        stock.quantity += quantity
        stock.save()

        serializer = self.get_serializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ConsumeProductView(generics.UpdateAPIView):
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated, IsConsumer]

    def update(self, request, *args, **kwargs):
        data = request.data
        warehouse_id = data.get('warehouse')
        product_id = data.get('product')
        quantity = data.get('quantity', 0)

        # Проверка, что склад существует
        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except Warehouse.DoesNotExist:
            return Response({"error": "Склад не найден."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что товар существует
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Товар не найден."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что количество положительное
        if quantity <= 0:
            return Response({"error": "Количество должно быть положительным."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Получение записи в Stock
        try:
            stock = Stock.objects.get(warehouse=warehouse, product=product)
        except Stock.DoesNotExist:
            return Response({"error": "Товар не доступен на данном складе."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Проверка, что доступно достаточно товара
        if stock.quantity < quantity:
            return Response({"error": "Недостаточно товара на складе."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Уменьшение количества товара
        stock.quantity -= quantity
        stock.save()

        serializer = self.get_serializer(stock)
        return Response(serializer.data, status=status.HTTP_200_OK)
