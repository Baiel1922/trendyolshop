from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, ListCreateAPIView,RetrieveDestroyAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from account.permissions import IsAuthorPermission, IsActivePermission
from rest_framework.views import APIView
from django.db.utils import IntegrityError
from time import time
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from .models import *
from .serializers import *
from parsers import TrendyolScraper, Scraper


class PermissionMixin:
    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAuthenticated, IsActivePermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission, ]
        else:
            permissions = [AllowAny]
        return [permission() for permission in permissions]


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    filter_class = ProductFilter

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RetriveReviewSerializer(instance)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def recomendation(self, request, pk):
        product_id = Product.objects.get(id=pk)
        category_of_product = product_id.category
        recomendation_product = Product.objects.filter(category=category_of_product)
        serializer = ProductSerializer(recomendation_product, many=True)

        return Response(serializer.data)

    @action(methods=['POST'], detail=True)
    def rating(self, request, pk):
        serializer = Review2Serializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj = Review2.objects.get(product=self.get_object(), user=request.user)
            obj.rating = request.data['rating']
        except Review2.DoesNotExist:
            obj = Review2(user=request.user, product=self.get_object(), rating=request.data['rating'])

        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)

    @action(methods=['POST'], detail=True)
    def like(self, request, pk):
        product = self.get_object()
        like_obj, _ = Like.objects.get_or_create(product=product, user=request.user)
        print(like_obj)
        like_obj.like = not like_obj.like
        like_obj.save()
        status = 'liked'
        if not like_obj.like:
            status = 'unliked'
        return Response({'status': status})

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class ReviewViewset(PermissionMixin, ModelViewSet):
    """
    Представление отзывов
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteView(ModelViewSet):
    """
    Представление избранных
    """
    permission_classes = [IsAuthorPermission, ]
    queryset = FavouriteProduct.objects.all()
    serializer_class = FavouriteProductSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class FavouriteDeleteUpdateRetriveView(RetrieveDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

class ImageView(PermissionMixin, ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AllSizesView(PermissionMixin, ModelViewSet):
    queryset = AllSizes.objects.all()
    serializer_class = ProductAllSizesSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class ParseCategory(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, format=None):
        scraper = Scraper()
        responce = scraper.parse_categories()
        return Response(responce)


class ParseColor(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, format=None):
        scraper = Scraper()
        responce = scraper.parse_colors()
        return Response(responce)


class ParseBrand(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, format=None):
        scraper = Scraper()
        responce = scraper.parse_brands()
        return Response(responce)


class ParseSize(APIView):
    permission_classes = [IsAdminUser, ]

    def get(self, request, format=None):
        scraper = Scraper()
        responce = scraper.parse_sizes()
        return Response(responce)


class ParseProduct(APIView):
    permission_classes = [IsAdminUser, ]

    def post(self, request, format=None):
        scraper = Scraper()
        data = request.data
        coefficient = data["coefficient"]
        coefficient = int(coefficient)
        responce = scraper.parse_products(coefficient)
        return Response(responce)


class BrandView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [AllowAny, ]


class ColorView(generics.ListAPIView):
    queryset = Color.objects.all()
    serializer_class = ColorSerializer
    permission_classes = [AllowAny, ]