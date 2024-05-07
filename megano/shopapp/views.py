from django.core.paginator import Paginator
from django.db.models import Count
from rest_framework import status, permissions, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Tag, Review, Category, Sale
from .serializers import ProductSerializer, ReviewSerializer, TagSerializer, CategorySerializer, SaleProductSerializer


class ProductDetailView(APIView):
    """
    Представление для отображения продукта.

    Позволяет получить информацию о конкретном продукте по его идентификатору.
    """
    serializer_class = ProductSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)

    def get(self, request, id):
        """
        Обработка GET-запроса для получения информации о продукте.
        Args:
           request: Запрос.
           id: Идентификатор продукта.
        Returns:
           Response: Статус выполнения операции и данные продукта или сообщение об ошибке.
        """
        try:
            print('try')
            product = Product.objects.get(id=id)
            print(product.title)
            serializer = ProductSerializer(product)
            print(serializer.data)
            print('ok')
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            print('error Product not found')
            return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class ProductReviewCreateView(APIView):
    """
    Представление для добавления отзыва о продукте.

    Позволяет пользователям добавлять отзывы о продуктах.
    """
    serializer_class = ReviewSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated] #пишем пермиш потому что сюда не авторизованные заходить не могут

    def test_func(self):
        """Проверяет, аутентифицирован ли пользователь."""

        return self.request.user.is_authenticated

    def post(self, request, id):
        """
        Обработка POST-запроса для создания отзыва о продукте.

        Args:
            request: Запрос.
            id: Идентификатор продукта, к которому относится отзыв.

        Returns:
            Response: Статус выполнения операции и данные созданного отзыва или ошибки валидации.
        """
        print('post')
        serializer = ReviewSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            print(serializer.is_valid())
            serializer.save(product_id=id)  # Furnizăm product_id când salvăm recenzia
            print('serializer saved')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print('error')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagListView(APIView):
    """
    Представление для отображения списка тегов.

    Обрабатывает GET-запрос и возвращает список всех тегов.
    """
    def get(self, request):
        """
        Обработка GET-запроса для получения списка всех тегов.
        Args:
            request: Запрос.
        Returns:
            Response: Список всех тегов в формате JSON.
        """
        print('tag')
        tags = Tag.objects.all()
        print(tags)
        serializer = TagSerializer(tags, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagDetailView(APIView):
    """
    Представление для отображения списка тегов.

    Обрабатывает GET-запрос и возвращает информацию о конкретном теге по его идентификатору.
    """
    def get(self, request, pk):
        """
        Обработка GET-запроса для получения информации о конкретном теге.
        Args:
            request: Запрос.
            pk (int): Идентификатор тега.
        Returns:
            Response: Информация о теге в формате JSON или код ошибки 404, если тег не найден.
        """
        try:
            print('try')
            tag = Tag.objects.get(pk=pk)
            print(tag)
            serializer = TagSerializer(tag)
            print(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist:
            print('error tag not found')
            return Response(status=status.HTTP_404_NOT_FOUND)


class CategoryAPIView(APIView):
    """
    Обработка GET-запроса для получения списка категорий и субкатегорий.
    Returns:
        Response: Список категорий и субкатегорий в формате JSON.
    """
    def get(self, request):
        """
        Обработка GET-запроса для получения списка категорий и субкатегорий.
        Returns:
            Response: Список категорий и субкатегорий в формате JSON.
        """
        print('ok')
        categories = Category.objects.all()
        print(categories)
        serializer = CategorySerializer(categories, many=True)
        print(serializer)
        print('yes')
        return Response(serializer.data, status=status.HTTP_200_OK)


class CatalogPagination(PageNumberPagination):
    """
       Пагинация для каталога товаров.
       Позволяет разбить список товаров на страницы с заданным количеством элементов на странице.
       """
    page_size = 20  # Numărul de elemente pe pagină
    page_size_query_param = 'limit'
    max_page_size = 1000  # Numărul maxim de elemente pe pagină

    def get_paginated_response(self, data) -> Response:
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
                'currentPage': self.page.number,
                'lastPage': last_page_number,
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

    filterset_fields = ['category', 'tags']
    search_fields = ['title', 'description', 'tags']
    ordering_fields = ['rating', 'price', 'reviews', 'date']
    ordering = ['date']

    def get_queryset(self):
        """
        Получение кастомного запроса к базе данных для получения списка товаров.
        Returns:
           QuerySet: Кастомный запрос к базе данных для получения списка товаров.
        """
        queryset = super().get_queryset()

        # Filtrare după nume
        name = self.request.query_params.get('filter[name]')
        if name:
            queryset = queryset.filter(title__icontains=name)

        # Filtrare după preț minim
        min_price = self.request.query_params.get('filter[minPrice]')
        if min_price is not None:
            queryset = queryset.filter(price__gte=min_price)

        # Filtrare după preț maxim
        max_price = self.request.query_params.get('filter[maxPrice]')
        if max_price is not None:
            queryset = queryset.filter(price__lte=max_price)

        # Filtrare după livrare gratuită
        free_delivery = self.request.query_params.get('filter[freeDelivery]')
        if free_delivery == 'true':
            queryset = queryset.filter(freeDelivery=True)

        # Filtrare după disponibilitate
        available = self.request.query_params.get('filter[available]')
        if available == 'true':
            queryset = queryset.filter(available=True)

        # Sortare
        sort = self.request.query_params.get('sort')
        if sort:
            queryset = queryset.order_by(sort)

        return queryset


class PopularProductsAPIView(APIView):
    """
    Представление API, чтобы получить популярные продукты.    """

    def get(self, request):
        """
        Получение и возврашение самые популярные продукты.
        """
        queryset = Product.objects.annotate(tag_count=Count('tags')).order_by('-tag_count')[:10]
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LimitedProductsAPIView(APIView):
    """
    API view pentru a obține produsele cu o limită specificată.
    """

    def get(self, request):
        """
        Obține și returnează toate produsele disponibile.
        """
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SaleAPIView(APIView):
    """
    API view pentru a obține produsele care sunt la vânzare, inclusiv informații despre vânzări.
    """
    def get(self, request: Request) -> Response:
        page_number = request.GET.get("currentPage", 1)
        print(page_number)
        paginator = Paginator(Sale.objects.all(), 10)
        page = paginator.page(page_number)
        serializer = SaleProductSerializer(page.object_list, many=True)
        result = {
            "items": serializer.data,
            "currentPage": page.number,
            "lastPage": paginator.num_pages
        }
        print(result)
        return Response(data=result, status=status.HTTP_200_OK)