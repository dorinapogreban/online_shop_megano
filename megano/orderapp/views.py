import random

from django.http import Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, PaymentSerializer, PaymentStatusSerializer, PaymentSomeoneSerializer
from shopapp.utils.cart import Cart


class OrdersAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(profile=request.user.profile).order_by('-createdAt')
        print(orders)
        serializer = OrderSerializer(orders, many=True)
        print(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        cart = Cart(request)
        print('Cart items:', cart)

        # Crearea comenzii
        order = Order.objects.create(profile=request.user.profile)

        print('Created order:', order)

        # # Salvăm instanța `Order` pentru a obține un ID (cheie primară)
        # order.save()
        for item in cart:
            product = item['product']
            count = item['count']
            price = product.price
            print('Adding product to order:', product, count, price)

            OrderItem.objects.create(order=order, product=product, price=price, count=count)  #, image=image_url

        # order.totalCost = order.calculate_total_cost()
        # print('Calculated totalCost:', order.totalCost)

        order.save()
        cart.clear()
        print(order)
        print('ok')
        return Response({'orderId': order.id}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for order in response.data:
            for product in order['products']:
                if 'images' not in product:
                    product['images'] = []  # Asigurați-vă că există o listă goală dacă nu sunt imagini
        return response


class OrderDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, id):
        try:
            print(Order.objects.get(id=id, profile=self.request.user.profile))
            # Obține comanda cu ID-ul specificat
            return Order.objects.get(id=id, profile=self.request.user.profile)
        except Order.DoesNotExist:
            # Ridică o excepție Http404 dacă comanda nu există
            raise Http404

    def get(self, request, id):
        # Obține comanda specificată și serializează-o
        order = self.get_object(id)
        print(order)
        serializer = OrderSerializer(order)
        print(serializer)

        return Response(serializer.data)

    def post(self, request, id):
        order = self.get_object(id)
        print(order)

        serializer = OrderSerializer(order, data=request.data, partial=True)
        print(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
            print(serializer)

            # Actualizează costul total după salvare
            delivery_type = request.data.get('deliveryType', order.deliveryType)
            print(order.deliveryType)
            order.totalCost = order.calculate_total_cost()
            print(order.totalCost)
            order.status = 'accepted'
            print(order.status)
            order.save()
            print(order)
            if order.paymentType == 'someone':
                redirect_url = f'payment-someone'
                print('redirect_url', redirect_url)
                order.status = 'confirmed'

                return Response({'orderId': order.id, 'redirect_url': redirect_url})

            return Response({'orderId': order.id, }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderHistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(profile__user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id, profile__user=request.user)
        print("Order fetched: ", order)
        payment_method = order.paymentType
        print('payment_method', payment_method)

        # if payment_method == 'someone':
        #     redirect_url = f'payment-someone/{id}'
        #     print('redirect_url', redirect_url)
        #     return Response({'redirect_url': redirect_url}, status=status.HTTP_302_FOUND)

        serializer = PaymentSerializer(data=request.data)
        print('serializer.is_valid()', serializer.is_valid())
        print(serializer.errors)

        if serializer.is_valid():
            if payment_method == 'online':
                print('payment_method', payment_method)
                card_number = serializer.validated_data.get('number')
                print('card_number', card_number)

                if Payment.objects.filter(order=order).exists():
                    return Response({'error': 'Payment already exists for this order'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if len(card_number) > 8 or not card_number.isdigit() or int(card_number) % 2 != 0:
                    return Response({'error': 'Invalid card number'}, status=status.HTTP_400_BAD_REQUEST)

                if int(card_number) % 10 != 0:
                    Payment.objects.create(order=order, **serializer.validated_data, status='confirmed')
                    return Response({'message': 'Awaiting payment confirmation from the payment system'},
                                    status=status.HTTP_200_OK)
                else:
                    Payment.objects.create(order=order, **serializer.validated_data, status='error',
                                           error_message='Payment error')
                    order.status = 'error'
                    return Response({'error': 'Payment error'}, status=status.HTTP_400_BAD_REQUEST)
            # elif payment_method == 'someone':
            #     random_account_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            #     return Response({'random_account_number': random_account_number}, status=status.HTTP_200_OK)
        order.status = 'confirmed'
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentSomeoneAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id, profile__user=request.user)
        print("Order fetched: ", order)

        random_account_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        print(random_account_number)

        order.status = 'confirmed'
        order.save()

        serializer = PaymentSomeoneSerializer(order)
        print(serializer)

        return Response({
            'random_account_number': random_account_number,
            'order': serializer.data
        }, status=status.HTTP_200_OK)


class PaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id, profile__user=request.user)
        print("Order fetched: ", order)
        payment_method = order.paymentType
        print('payment_method', payment_method)

        # if payment_method == 'someone':
        #     redirect_url = f'payment-someone/{id}'
        #     print('redirect_url', redirect_url)
        #     return Response({'redirect_url': redirect_url}, status=status.HTTP_302_FOUND)

        serializer = PaymentSerializer(data=request.data)
        print('serializer.is_valid()', serializer.is_valid())
        print(serializer.errors)

        if serializer.is_valid():
            if payment_method == 'online':
                print('payment_method', payment_method)
                card_number = serializer.validated_data.get('number')
                print('card_number', card_number)

                if Payment.objects.filter(order=order).exists():
                    return Response({'error': 'Payment already exists for this order'},
                                    status=status.HTTP_400_BAD_REQUEST)

                if len(card_number) > 8 or not card_number.isdigit() or int(card_number) % 2 != 0:
                    return Response({'error': 'Invalid card number'}, status=status.HTTP_400_BAD_REQUEST)

                if int(card_number) % 10 != 0:
                    Payment.objects.create(order=order, **serializer.validated_data, status='confirmed')
                    return Response({'message': 'Awaiting payment confirmation from the payment system'},
                                    status=status.HTTP_200_OK)
                else:
                    Payment.objects.create(order=order, **serializer.validated_data, status='error',
                                           error_message='Payment error')
                    order.status = 'error'
                    return Response({'error': 'Payment error'}, status=status.HTTP_400_BAD_REQUEST)
            # elif payment_method == 'someone':
            #     random_account_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            #     return Response({'random_account_number': random_account_number}, status=status.HTTP_200_OK)
        order.status = 'confirmed'
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentSomeoneAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id):
        order = get_object_or_404(Order, id=id, profile__user=request.user)
        print("Order fetched: ", order)

        random_account_number = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        print(random_account_number)

        order.status = 'confirmed'
        order.save()

        serializer = PaymentSomeoneSerializer(order)
        print(serializer)

        return Response({
            'random_account_number': random_account_number,
            'order': serializer.data
        }, status=status.HTTP_200_OK)


class ProgressPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        print("Fetching progress for order id:", id)
        order = get_object_or_404(Order, id=id, profile__user=request.user)
        payments = Payment.objects.filter(order=order).order_by('-created_at')

        if not payments.exists():
            print("No payments found for order id:", id)
            return Response({'status': 'No payment found'}, status=status.HTTP_404_NOT_FOUND)

        latest_payment = payments.first()
        serializer = PaymentStatusSerializer(latest_payment)
        print("Returning payment status for order id:", id)
        return Response(serializer.data, status=status.HTTP_200_OK)
class ProgressPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id):
        print("Fetching progress for order id:", id)
        order = get_object_or_404(Order, id=id, profile__user=request.user)
        payments = Payment.objects.filter(order=order).order_by('-created_at')

        if not payments.exists():
            print("No payments found for order id:", id)
            return Response({'status': 'No payment found'}, status=status.HTTP_404_NOT_FOUND)

        latest_payment = payments.first()
        serializer = PaymentStatusSerializer(latest_payment)
        print("Returning payment status for order id:", id)
        return Response(serializer.data, status=status.HTTP_200_OK)