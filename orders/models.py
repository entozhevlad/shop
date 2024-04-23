from django.db import models
from shop.models import Product
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, null=True, default=None)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    DELIVERY_CHOICES = ( ('mail', 'Почтой'), ('courier', 'Курьером'), ('pickup', 'Самовывоз'))
    delivery_prices = {
        'mail': 5,
        'courier': 10,
        'pickup': 0,
    }
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='pickup')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
        db_table = 'order'  # Новое название таблицы

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        delivery_price = Order.delivery_prices.get(self.delivery_method, 0)
        items_cost = sum(item.get_cost() for item in self.items.all())
        total_cost = items_cost + delivery_price
        return total_cost


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


