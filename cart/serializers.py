from django.shortcuts import get_object_or_404
from rest_framework import serializers
from product.models import Product, AllSizes
from product.serializers import ProductSerializer
from .models import CartItem, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

class CartItemSerializer(serializers.ModelSerializer):
    """
    serializer for cartitem that serialize all fields in 'CartItem' class
    model and add 'product' as relation
    """
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'quantity', 'product', 'size')

class CartItemAddSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    size_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ('quantity', 'product_id', 'size_id')
        extra_kwargs = {
            'quantity': {'required': True},
            'product_id': {'required': True},
            'size_id': {'required': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        product = get_object_or_404(Product, id=validated_data['product_id'])
        size = get_object_or_404(AllSizes, id=validated_data['size_id'], product=product)
        if size.in_stock is False:
            raise serializers.ValidationError(
                {'not available': 'the product is not available.'})

        cart_item = CartItem.objects.create(
            product=product,
            size=size,
            user=user,
            quantity=validated_data['quantity']
            )
        cart_item.save()
        cart_item.add_amount()
        return cart_item

