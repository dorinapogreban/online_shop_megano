from rest_framework import serializers
from .models import Order, OrderItem, Payment, PaymentSomeone
from shopapp.serializers import ProductSerializer, ImageSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор для элементов заказа"""

    product = ProductSerializer()  # Сериализатор для продукта
    images = serializers.SerializerMethodField()  # Поле для получения изображений

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "price", "count", "images"]

    def get_images(self, obj):
        """Метод для получения изображений продукта"""
        images = (
            obj.product.images.all()
        )  # Предполагается, что есть отношение ForeignKey или ManyToMany к изображениям
        return ImageSerializer(images, many=True).data if images else []


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор для заказов"""

    deliveryType = serializers.ChoiceField(
        choices=Order.DELIVERY_CHOICES, required=False, allow_null=True
    )  # Тип доставки
    paymentType = serializers.ChoiceField(
        choices=Order.PAYMENT_CHOICES, required=False, allow_null=True
    )  # Тип оплаты
    status = serializers.ChoiceField(
        choices=Order.STATUS_CHOICES, required=False, allow_null=True
    )  # Статус заказа
    city = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )  # Город
    address = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )  # Адрес
    totalCost = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )  # Общая стоимость
    fullName = serializers.CharField(
        source="profile.fullName", read_only=True
    )  # Полное имя пользователя
    email = serializers.CharField(
        source="profile.email", read_only=True
    )  # Электронная почта пользователя
    phone = serializers.CharField(
        source="profile.phone", read_only=True
    )  # Телефон пользователя
    products = OrderItemSerializer(
        many=True, source="products_in_order", read_only=True
    )  # Продукты в заказе

    class Meta:
        model = Order
        fields = [
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        ]

    def to_representation(self, instance):
        """Преобразование представления объекта"""
        ret = super().to_representation(instance)
        ret["totalCost"] = (
            instance.calculate_total_cost()
        )  # Убедитесь, что правильно вызывается функция расчета
        return ret


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    number = serializers.CharField(max_length=8)  # Номер карты

    class Meta:
        model = Payment
        fields = ["number", "name", "month", "year", "code"]

    def validate_number(self, value):
        """Валидация номера карты"""
        if not value.isdigit():
            raise serializers.ValidationError("Card number must contain only digits")
        if len(value) > 8:
            raise serializers.ValidationError(
                "Card number must not be longer than 8 digits"
            )
        if int(value) % 2 != 0:
            raise serializers.ValidationError("Card number must be even")
        return value


class PaymentSomeoneSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей от другого лица"""

    class Meta:
        model = PaymentSomeone
        fields = ["number", "status", "error_message", "created_at"]


class PaymentStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для статуса платежа"""

    order_id = serializers.IntegerField(source="order.id")  # ID заказа

    class Meta:
        model = Payment
        fields = ["order_id", "status", "error_message"]
