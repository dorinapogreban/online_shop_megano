from django.urls import path, include
from .views import (
    OrdersAPIView,
    OrderDetailAPIView,
    PaymentAPIView,
    PaymentSomeoneAPIView,
    ProgressPaymentView,
    OrderHistoryAPIView,
)


"""
Настройка маршрутов URL для приложения заказов.
"""

app_name = "orderapp"

urlpatterns = [
    path("orders", OrdersAPIView.as_view(), name="orders"),
    path("order/<int:id>", OrderDetailAPIView.as_view(), name="order_detail"),
    path("order/<int:id>", OrderDetailAPIView.as_view(), name="put_order"),
    path("__debug__/", include("debug_toolbar.urls")),
    path("payment/<int:id>", PaymentAPIView.as_view(), name="payment"),
    path("history-order", OrderHistoryAPIView.as_view(), name="history-order"),
    path("payment-someone", PaymentSomeoneAPIView.as_view(), name="payment-someone"),
    path(
        "progress-payment/<int:id>",
        ProgressPaymentView.as_view(),
        name="progress-payment",
    ),
]
