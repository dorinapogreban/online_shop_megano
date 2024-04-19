from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Tag, Review
from .serializers import ProductSerializer, ReviewSerializer, TagSerializer


class ProductDetailView(APIView):

    serializer_class = ProductSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    def get(self, request, id):
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
    serializer_class = ReviewSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    def post(self, request, id):
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

    # def get(self, request, id):
    #     try:
    #         print('try')
    #         product = Product.objects.get(id=id)
    #         print(product)
    #         reviews = product.reviews.all()
    #         print(reviews)
    #         serializer = ReviewSerializer(reviews, many=True)
    #         print(serializer)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Product.DoesNotExist:
    #         print('error')
    #         return Response({"message": "Product not found"}, status=status.HTTP_404_NOT_FOUND)


class TagListView(APIView):
    def get(self, request):
        print('tag')
        tags = Tag.objects.all()
        print(tags)
        serializer = TagSerializer(tags, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagDetailView(APIView):
    def get(self, request, pk):
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