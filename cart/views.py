from rest_framework.filters import SearchFilter
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem
from product.models import Product, AllSizes
from .serializers import *
# Create your views here.
class CartItemView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = [SearchFilter, ]
    search_fields = [
        'product__name', 'product__description', 'product__category__title']

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)

class CartItemAddView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemAddSerializer
    permission_classes = (IsAuthenticated, )


class CartItemDelView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = CartItem.objects.all()

    def delete(self, request, pk, format=None):
        user = request.user
        cart_item = CartItem.objects.filter(user=user)
        target_product = get_object_or_404(cart_item, pk=pk)
        target_product.delete()
        return Response(status=status.HTTP_200_OK, data={"detail": "deleted"})

class CartItemAddOneView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, format=None):
        user = request.user
        cart_item = CartItem.objects.filter(user=user)
        target_product = cart_item.get(pk=pk)
        product = get_object_or_404(Product, id=target_product.product.id)
        size = get_object_or_404(AllSizes, id=target_product.size.id)
        if size.in_stock is False:
            return Response(
                data={
                    "detail": "this item is sold out try another one !",
                    "code": "sold_out"})

        target_product.quantity = target_product.quantity + 1
        target_product.save()
        return Response(
            status=status.HTTP_226_IM_USED,
            data={"detail": 'one object added', "code": "done"})

class CartItemReduceOneView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, pk, format=None):
        user = request.user
        cart_item = CartItem.objects.filter(user=user)
        target_product = cart_item.get(pk=pk)
        # product = get_object_or_404(Product, id=target_product.product.id)
        if target_product.quantity == 0:
            return Response(
                data={
                    "detail": "there is no more item like this in tour cart",
                    "code": "no_more"})

        target_product.quantity = target_product.quantity - 1
        target_product.save()
        return Response(
            status=status.HTTP_226_IM_USED,
            data={
                "detail": 'one object deleted',
                "code": "done"
            })
