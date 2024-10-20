from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('supplier', 'Поставщик'),
        ('consumer', 'Потребитель'),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        null=True,
        blank=True
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

User = get_user_model()

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(User, related_name='warehouses', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Stock(models.Model):
    warehouse = models.ForeignKey('Warehouse', related_name='stocks', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='stocks', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product')

    def __str__(self):
        return f"{self.product.name} in {self.warehouse.name}: {self.quantity}"
