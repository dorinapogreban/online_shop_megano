from django.db import models
from shopapp.models import Product
from myauth.models import Profile
from django.utils import timezone



class Order(models.Model):
    DELIVERY_CHOICES = [
        ('ordinary', 'Free Delivery'),
        ('express', 'Express Delivery')
    ]
    PAYMENT_CHOICES = [
        ('online', 'Online Card'),
        ('someone', 'Online Account')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('confirmed', 'Confirmed'),
        ('error', 'Error')
    ]
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    deliveryType = models.CharField(max_length=10, choices=DELIVERY_CHOICES, default='ordinary',
                                    verbose_name="Delivery Type", null=True, blank=True,)
    paymentType = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='online',
                                   verbose_name="Payment Type", null=True, blank=True,)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    city = models.CharField(max_length=100, verbose_name="City", null=True, blank=True,)
    address = models.TextField(max_length=255, null=True, blank=True, verbose_name="Address")
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name="Profile")
    # deliveryCost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    totalCost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('-createdAt',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def calculate_delivery_cost(self):
        # Calcularea costului de livrare în funcție de tipul de livrare
        if self.deliveryType == 'ordinary':
            return 200 if self.calculate_total_cost_without_delivery() < 2000 else 0
        elif self.deliveryType == 'express':
            return 500
        return 0

    def calculate_total_cost_without_delivery(self):
        # Calcularea costului total al produselor din comandă fără costul de livrare
        total_cost = sum(item.price * item.count for item in self.products_in_order.all())
        print('total_cost', total_cost)
        return total_cost

    def calculate_total_cost(self):
        # Calcularea costului total al comenzii, inclusiv costul de livrare
        total_cost_without_delivery = self.calculate_total_cost_without_delivery()
        delivery_cost = self.calculate_delivery_cost()
        print('total_cost_without_delivery', total_cost_without_delivery)
        print('delivery_cost', delivery_cost)
        print('totalCost', total_cost_without_delivery + delivery_cost)
        return total_cost_without_delivery + delivery_cost

    def __str__(self):
        return 'Order {}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products_in_order', verbose_name="Order")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Product")
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Price")
    count = models.PositiveIntegerField(default=1, verbose_name="Quantity product in order")
    image = models.ImageField(upload_to="order_item_images/", blank=True, null=True, verbose_name="Image")

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return '{}'.format(self.id)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    number = models.CharField(max_length=16, verbose_name="Card Number")
    name = models.CharField(max_length=255, verbose_name="Name of card owner")
    month = models.CharField(max_length=2, verbose_name="Month until card is valid")
    year = models.CharField(max_length=4, verbose_name="Year until card is valid")
    code = models.CharField(max_length=3, verbose_name="Secret verification code")
    status = models.CharField(max_length=20,
                              choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('error', 'Error')],
                              default='pending')
    error_message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f"Payment for Order ID: {self.order.id}"


# class PaymentSomeone(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     number = models.CharField(max_length=8, verbose_name="Card Number")
#     status = models.CharField(max_length=20, default='pending')
#     error_message = models.CharField(max_length=255, blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = 'Payment Someone'
#         verbose_name_plural = 'Payments Someone'