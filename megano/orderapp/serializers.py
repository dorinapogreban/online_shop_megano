import random

from rest_framework import serializers
from .models import Order, OrderItem, Payment
from shopapp.serializers import ProductSerializer, ImageSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    images = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'price', 'count', 'images']

    def get_images(self, obj):
        images = obj.product.images.all()  # Asumând că aveți o relație de tip `ForeignKey` sau `ManyToMany` către imagini
        return ImageSerializer(images, many=True).data if images else []


class OrderSerializer(serializers.ModelSerializer):
    # Уточняем типы данных для каждого поля
    deliveryType = serializers.ChoiceField(choices=Order.DELIVERY_CHOICES, required=False, allow_null=True)
    paymentType = serializers.ChoiceField(choices=Order.PAYMENT_CHOICES, required=False, allow_null=True)
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, required=False, allow_null=True)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    totalCost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    fullName = serializers.CharField(source='profile.fullName', read_only=True)
    email = serializers.CharField(source='profile.email', read_only=True)
    phone = serializers.CharField(source='profile.phone', read_only=True)
    products = OrderItemSerializer(many=True, source='products_in_order', read_only=True)


    class Meta:
        model = Order
        fields = ['id', 'createdAt', 'fullName', 'email', 'phone', 'deliveryType',
                  'paymentType', 'totalCost', 'status', 'city', 'address', 'products']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['totalCost'] = instance.calculate_total_cost()  # Asigură-te că apelezi corect funcția de calcul
        return ret


class PaymentSerializer(serializers.ModelSerializer):
    number = serializers.CharField(max_length=8)

    class Meta:
        model = Payment
        fields = ['number', 'name', 'month', 'year', 'code']

    def validate_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Card number must contain only digits")
        if len(value) > 8:
            raise serializers.ValidationError("Card number must not be longer than 8 digits")
        if int(value) % 2 != 0:
            raise serializers.ValidationError("Card number must be even")
        return value


class PaymentSomeoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['number']


class PaymentStatusSerializer(serializers.ModelSerializer):
    order_id = serializers.IntegerField(source='order.id')

    class Meta:
        model = Payment
        fields = ['order_id', 'status', 'error_message']