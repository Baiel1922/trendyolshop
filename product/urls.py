from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'review', ReviewViewset)
router.register(r'size', AllSizesView)
router.register(r'image', ImageView)
router.register(r'favorite', FavouriteView)

urlpatterns = [
    path('category/', CategoryView.as_view()),
    path('', include(router.urls)),
    path('parse_category/', ParseCategory.as_view()),
    path('parse_color/', ParseColor.as_view()),
    path('parse_brand/', ParseBrand.as_view()),
    path('parse_size/', ParseSize.as_view()),
    path('parse_product/', ParseProduct.as_view()),
    path('brand-list/', BrandView.as_view()),
    path('color-list/', ColorView.as_view()),
]
