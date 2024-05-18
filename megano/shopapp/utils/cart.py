from decimal import Decimal
from django.conf import settings
from ..models import Product


class Cart(object):
    """
    Класс, представляющий корзину покупок пользователя.
    """
    def __init__(self, request):
        """
        Инициализирует корзину покупок.

        Args:
            request: Запрос Django.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product_id, count=1):
        """
        Добавляет товар в корзину.

        Args:
            product_id (int): ID продукта.
            count (int): Количество продукта (по умолчанию 1).
        """
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'count': count}
        else:
            self.cart[product_id]['count'] += count
        self.save()

    def save(self):
        """
        Сохраняет состояние корзины в сессии.
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product_id):
        """
        Удаляет товар из корзины.

        Args:
            product_id (int): ID продукта.
        """
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """
        Возвращает итератор для товаров в корзине.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            yield item

    def __len__(self):
        """
        Возвращает общее количество товаров в корзине.
        """
        return sum(item['count'] for item in self.cart.values())

    def get_total_price(self):
        """
        Возвращает общую стоимость товаров в корзине.
        """
        return sum(Decimal(item['product'].price) * item['count'] for item in self.cart.values())
