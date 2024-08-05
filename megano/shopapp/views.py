from django.core.paginator import Paginator

from rest_framework import status, permissions, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, Tag, Category, Sale, Banner
from .serializers import (
    ProductSerializer,
    ReviewSerializer,
    TagSerializer,
    CategorySerializer,
    SaleProductSerializer,
    BannerSerializer,
)
from .utils.cart import Cart


class ProductDetailView(APIView):
    """
    Представление для отображения продукта.

    Позволяет получить информацию о конкретном продукте по его идентификатору.
    """

    serializer_class = ProductSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get(self, request: Request, id: int) -> Response:
        """
        Обработка GET-запроса для получения информации о продукте.
        Args:
           request: Запрос.
           id: Идентификатор продукта.
        Returns:
           Response: Статус выполнения операции и данные продукта или сообщение об ошибке.
        """
        try:
            product = Product.objects.get(id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )


class ProductReviewCreateView(APIView):
    """
    Представление для добавления отзыва о продукте.

    Позволяет пользователям добавлять отзывы о продуктах.
    """

    serializer_class = ReviewSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permission_classes = [
        permissions.IsAuthenticated
    ]  # пишем пермиш потому что сюда не авторизованные заходить не могут

    def test_func(self):
        """Проверяет, аутентифицирован ли пользователь."""

        return self.request.user.is_authenticated

    def post(self, request: Request, id: int) -> Response:
        """
        Обработка POST-запроса для создания отзыва о продукте.

        Args:
            request: Запрос.
            id: Идентификатор продукта, к которому относится отзыв.

        Returns:
            Response: Статус выполнения операции и данные созданного отзыва или ошибки валидации.
        """
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                product_id=id
            )  # Предоставляем product_id при сохранении отзыва
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagListView(APIView):
    """
    Представление для отображения списка тегов.

    Обрабатывает GET-запрос и возвращает список всех тегов.
    """

    def get(self, request: Request) -> Response:
        """
        Обработка GET-запроса для получения списка всех тегов.
        Args:
            request: Запрос.
        Returns:
            Response: Список всех тегов в формате JSON.
        """
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagDetailView(APIView):
    """
    Представление для отображения списка тегов.

    Обрабатывает GET-запрос и возвращает информацию о конкретном теге по его идентификатору.
    """

    def get(self, request: Request, pk: int) -> Response:
        """
        Обработка GET-запроса для получения информации о конкретном теге.
        Args:
            request: Запрос.
            pk (int): Идентификатор тега.
        Returns:
            Response: Информация о теге в формате JSON или код ошибки 404, если тег не найден.
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryAPIView(APIView):
    """
    Обработка GET-запроса для получения списка категорий и субкатегорий.
    Returns:
        Response: Список категорий и субкатегорий в формате JSON.
    """

    def get(self, request: Request) -> Response:
        """
        Обработка GET-запроса для получения списка категорий и субкатегорий.
        Returns:
            Response: Список категорий и субкатегорий в формате JSON.
        """
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CatalogPagination(PageNumberPagination):
    """
    Пагинация для каталога товаров.
    Позволяет разбить список товаров на страницы с заданным количеством элементов на странице.
    """

    page_size = 20  # Количество элементов на странице
    page_size_query_param = "limit"
    max_page_size = 1000  # Максимальное количество элементов на странице

    def get_paginated_response(self, data: list) -> Response:
        """
        Генерирует ответ с данными и информацией о пагинации.
        Args:
            data (list): Список данных для текущей страницы.
        Returns:
            Response: Ответ с данными и информацией о пагинации.
        """
        last_page_number = self.page.paginator.num_pages
        return Response(
            {
                "items": data,
                "currentPage": self.page.number,
                "lastPage": last_page_number,
            }
        )


class CatalogAPIView(generics.ListAPIView):
    """
    Представление API для отображения каталога товаров.

    Позволяет получать список товаров с возможностью фильтрации, сортировки и пагинации.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    pagination_class = CatalogPagination

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по категории и подкатегории
        queryset = self.filter_by_category(queryset)

        # Применение других фильтров
        queryset = self.apply_filters(queryset)

        return queryset

    def filter_by_category(self, queryset):
        category_id = self.request.query_params.get("category")
        subcategory_id = self.request.query_params.get("subcategory")

        if subcategory_id:
            queryset = queryset.filter(category__subcategories=subcategory_id)
        elif category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def apply_filters(self, queryset):
        # Фильтрация по имени
        name = self.request.query_params.get("filter[name]")
        if name:
            queryset = queryset.filter(title__icontains=name)

        # Фильтрация по минимальной цене
        min_price = self.request.query_params.get("filter[minPrice]")
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        # Фильтрация по максимальной цене
        max_price = self.request.query_params.get("filter[maxPrice]")
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        # Фильтрация по бесплатной доставке
        free_delivery = self.request.query_params.get("filter[freeDelivery]")
        if free_delivery == "true":
            queryset = queryset.filter(freeDelivery=True)

        # Фильтрация по наличию
        available = self.request.query_params.get("filter[available]")
        if available == "true":
            queryset = queryset.filter(available=True)

        # Сортировка
        sort_by = self.request.query_params.get("sort")
        sort_type = self.request.query_params.get("sortType")

        if sort_by:
            if sort_type == "dec":
                sort_by = f"-{sort_by}"
            queryset = queryset.order_by(sort_by)

        return queryset


class PopularProductsAPIView(APIView):
    """
    Представление API, чтобы получить популярные продукты."""

    def get(self, request: Request) -> Response:
        """
        Получает первые 8 продуктов, отсортированных по sort_index и sales_count.
        """
        top_products = Product.top_products(limit=8)
        serializer = ProductSerializer(top_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LimitedProductsAPIView(APIView):
    """
    API представление для получения продуктов с указанным лимитом.
    """

    def get(self, request: Request) -> Response:
        """
        Получает и возвращает все доступные продукты.
        """
        limited_products = Product.objects.filter(limited_edition=True)[
            :16
        ]  # Первые 16 продуктов с ограниченным тиражом
        serializer = ProductSerializer(limited_products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaleAPIView(APIView):
    """
    API представление для получения продуктов, которые находятся на распродаже, включая информацию о скидках.
    """

    def get(self, request: Request) -> Response:
        """
        Получает продукты на распродаже с информацией о скидках.
        """
        page_number = request.GET.get("currentPage", 1)
        paginator = Paginator(Sale.objects.all(), 10)
        page = paginator.page(page_number)
        serializer = SaleProductSerializer(page.object_list, many=True)
        result = {
            "items": serializer.data,
            "currentPage": page.number,
            "lastPage": paginator.num_pages,
        }
        return Response(data=result, status=status.HTTP_200_OK)


class BannerList(APIView):
    """
    API представление для получения списка баннеров.
    """

    def get(self, request: Request) -> Response:
        """
        Получает список всех баннеров.
        """
        banners = Banner.objects.all()
        serializer = BannerSerializer(banners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartAPIView(APIView):
    """
    API представление для работы с корзиной пользователя.
    """

    def get(self, request: Request) -> Response:
        """
        Получает содержимое корзины пользователя.
        """
        cart = Cart(request)
        basket_items = cart.__iter__()
        serialized_items = []
        for item in basket_items:
            product = item["product"]
            serializer = ProductSerializer(product)
            serialized_item = serializer.data
            serialized_item["count"] = item["count"]
            serialized_items.append(serialized_item)
        return Response(serialized_items, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """
        Добавляет товар в корзину.
        """
        product_id = request.data.get("id")
        count = request.data.get("count")
        if product_id and count:
            try:
                product = Product.objects.get(id=product_id)
                cart = Cart(request)
                cart.add(product_id, count)
                return Response(
                    {"message": "Product added to basket"}, status=status.HTTP_200_OK
                )
            except Product.DoesNotExist:
                return Response(
                    {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request: Request) -> Response:
        """
        Удаляет товар из корзины.
        """
        product_id = request.data.get("id")
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                cart = Cart(request)
                cart.remove(product_id)
                return Response(
                    {"message": "Product removed from basket"},
                    status=status.HTTP_200_OK,
                )
            except Product.DoesNotExist:
                return Response(
                    {"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST
            )
