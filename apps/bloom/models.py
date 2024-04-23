from django.db import models
from uuid import uuid4

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Payment(models.Model):

    uid = models.UUIDField(default=uuid4, editable=False)

    @property
    def merchant_uid(self):
        return self.uid

    name = models.CharField(max_length=255)  # 추후 상품 객체로 수정해야 함
    amount = models.PositiveIntegerField()

    STATUS_CHOICES = (
        ("ready", "미결제"),
        ("paid", "결제 완료"),
        ("cancelled", "결제 취소"),
        ("failed", "결제 실패"),
    )

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="ready", db_index=True
    )
    is_paid = models.BooleanField(default=False, db_index=True)


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()

    STATUS_CHOICES = (
        ('in_stock', '재고 있음'),
        ('sold_out', '품절'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_constraint=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sold_out')



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    thumbnail_image = models.ImageField(upload_to='products/photo/%Y/%m/%d/')
    detail_image = models.ImageField(upload_to='products/photo/%Y/%m/%d/')


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_constraint=False)
    quantity =models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.pk} : {self.product.name} - {self.product.name}'



class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=False)
    amount = models.PositiveIntegerField("결제 금액")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class OrderedProduct(models.Model):
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, db_constraint=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_constraint=False)
    
    name = models.CharField("상품명", max_length=100, help_text='주문 시점의 상품명')
    price = models.PositiveIntegerField("상품 가격", help_text='주문 시점의 상품 가격')
    quantity = models.PositiveIntegerField("주문 수량")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)