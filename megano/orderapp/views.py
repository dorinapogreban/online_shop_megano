import random
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem, Payment, PaymentSomeone
from .serializers import (
    OrderSerializer,
    PaymentSerializer,
    PaymentStatusSerializer,
    PaymentSomeoneSerializer,
)
from shopapp.utils.cart import Cart


class OrdersAPIView(APIView):
    """
    Класс для обработки запросов на получение и создание заказов.

    Обрабатывает GET-запросы для получения всех заказов текущего пользователя
    и POST-запросы для создания нового заказа.
    """

    permission_classes = [permissions.IsAuthenticated]  # Требуется аутентификация

    def get(self, request: Request) -> Response:
        """
        Метод для получения всех заказов текущего пользователя.

        Args:
            request: Запрос.

        Returns:
            Response: Список всех заказов текущего пользователя в формате JSON.
        """
        orders = Order.objects.filter(profile=request.user.profile).order_by(
            "-createdAt"
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """
        Метод для создания нового заказа.

        Args:
            request: Запрос.

        Returns:
            Response: Идентификатор созданного заказа в формате JSON.
        """
        cart = Cart(request)
        # Создание заказа
        order = Order.objects.create(profile=request.user.profile)

        for item in cart:
            product = item["product"]
            count = item["count"]
            price = product.price
            OrderItem.objects.create(
                order=order, product=product, price=price, count=count
            )

        order.save()
        cart.clear()
        return Response({"orderId": order.id}, status=status.HTTP_201_CREATED)

    def list(self, request: Request, *args, **kwargs) -> Response:
        """
        Метод для получения списка заказов с изображениями продуктов.

        Args:
            request: Запрос.

        Returns:
            Response: Список заказов с изображениями продуктов в формате JSON.
        """
        response = super().list(request, *args, **kwargs)
        for order in response.data:
            for product in order["products"]:
                if "images" not in product:
                    product["images"] = (
                        []
                    )  # Убедитесь, что есть пустой список, если нет изображений
        return response


class OrderDetailAPIView(APIView):
    """
    Класс для обработки запросов на получение и обновление конкретного заказа.

    Обрабатывает GET-запросы для получения данных конкретного заказа
    и POST-запросы для обновления данных конкретного заказа.
    """

    permission_classes = [permissions.IsAuthenticated]  # Требуется аутентификация

    def get_object(self, id: int) -> Order:
        """
        Метод для получения объекта заказа по ID.

        Args:
            id: Идентификатор заказа.

        Returns:
            Order: Объект заказа.

        Raises:
            Http404: Если заказ не найден.
        """
        try:
            return Order.objects.get(id=id, profile=self.request.user.profile)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request: Request, id: int) -> Response:
        """
        Метод для получения данных конкретного заказа.

        Args:
            request: Запрос.
            id: Идентификатор заказа.

        Returns:
            Response: Данные заказа в формате JSON.
        """
        order = self.get_object(id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def post(self, request: Request, id: int) -> Response:
        """
        Метод для обновления данных конкретного заказа.

        Args:
            request: Запрос.
            id: Идентификатор заказа.

        Returns:
            Response: Идентификатор обновленного заказа в формате JSON.
        """
        order = self.get_object(id)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # Обновление общей стоимости после сохранения
            delivery_type = request.data.get("deliveryType", order.deliveryType)
            order.totalCost = order.calculate_total_cost()
            order.status = "accepted"
            order.save()
            if order.paymentType == "someone":
                redirect_url = "payment-someone"
                order.status = "confirmed"
                return Response({"orderId": order.id, "redirect_url": redirect_url})
            return Response({"orderId": order.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderHistoryAPIView(APIView):
    """
    Класс для обработки запросов на получение истории заказов пользователя.

    Обрабатывает GET-запросы для получения всех заказов текущего пользователя.
    """

    permission_classes = [permissions.IsAuthenticated]  # Требуется аутентификация

    def get(self, request: Request) -> Response:
        """
        Метод для получения всех заказов текущего пользователя.

        Args:
            request: Запрос.

        Returns:
            Response: Список всех заказов текущего пользователя в формате JSON.
        """
        orders = Order.objects.filter(profile__user=request.user).order_by(
            "-created_at"
        )
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentAPIView(APIView):
    """
    Класс для обработки запросов на создание платежа.

    Обрабатывает POST-запросы для создания нового платежа.
    """

    permission_classes = [permissions.IsAuthenticated]  # Требуется аутентификация

    def post(self, request: Request, id: int) -> Response:
        """
        Метод для создания нового платежа.

        Args:
            request: Запрос.
            id: Идентификатор заказа.

        Returns:
            Response: Сообщение об успешном создании платежа или сообщение об ошибке в формате JSON.
        """
        order = get_object_or_404(Order, id=id, profile__user=request.user)
        payment_method = order.paymentType
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            if payment_method == "online":
                card_number = serializer.validated_data.get("number")

                if Payment.objects.filter(order=order).exists():
                    return Response(
                        {"error": "Payment already exists for this order"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if (
                    len(card_number) > 8
                    or not card_number.isdigit()
                    or int(card_number) % 2 != 0
                ):
                    return Response(
                        {"error": "Invalid card number"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if int(card_number) % 10 != 0:
                    Payment.objects.create(
                        order=order, **serializer.validated_data, status="confirmed"
                    )
                    return Response(
                        {
                            "message": "Awaiting payment confirmation from the payment system"
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    Payment.objects.create(
                        order=order,
                        **serializer.validated_data,
                        status="error",
                        error_message="Payment error"
                    )
                    order.status = "error"
                    return Response(
                        {"error": "Payment error"}, status=status.HTTP_400_BAD_REQUEST
                    )

        order.status = "confirmed"
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentSomeoneAPIView(APIView):
    """
    Класс для обработки запросов на создание платежа от другого лица.

    Обрабатывает POST-запросы для создания нового платежа от другого лица.
    """

    permission_classes = [permissions.IsAuthenticated]  # Требуется аутентификация

    def post(self, request: Request) -> Response:
        """
        Метод для создания нового платежа от другого лица.

        Args:
            request: Запрос.

        Returns:
            Response: Данные о платеже от другого лица в формате JSON.
        """
        order_id = request.data.get("order_id")
        if not order_id:
            return Response(
                {"error": "Order ID is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        order = get_object_or_404(Order, id=order_id, profile__user=request.user)
        random_account_number = "".join([str(random.randint(0, 9)) for _ in range(8)])
        payment_someone, created = PaymentSomeone.objects.get_or_create(order=order)
        payment_someone.number = random_account_number
        payment_someone.status = "confirmed"
        payment_someone.save()
        serializer = PaymentSomeoneSerializer(payment_someone)

        return Response(
            {
                "random_account_number": random_account_number,
                "payment": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ProgressPaymentView(APIView):
    """
    Класс для получения статуса платежа.

    Обрабатывает GET-запросы для получения прогресса платежа.
    """

    permission_classes = [permissions.IsAuthenticated]  # Требуется аутентификация

    def get(self, request: Request, id: int) -> Response:
        """
        Метод для получения прогресса платежа.

        Args:
            request: Запрос.
            id: Идентификатор заказа.

        Returns:
            Response: Статус последнего платежа в формате JSON.

        Raises:
            Http404: Если заказ не найден.
        """
        try:
            order = get_object_or_404(Order, id=id, profile__user=request.user)
            payments = Payment.objects.filter(order=order).order_by("-created_at")

            if not payments.exists():
                return Response(
                    {"status": "No payment found"}, status=status.HTTP_404_NOT_FOUND
                )

            latest_payment = payments.first()
            serializer = PaymentStatusSerializer(latest_payment)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            raise Http404
