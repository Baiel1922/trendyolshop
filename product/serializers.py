from rest_framework import serializers
from .models import *


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_title(self, title):
        if Category.objects.filter(slug=title.lower()).exists():
            raise serializers.ValidationError('Такое название уже существует')
        return title

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if not instance.parent:
            representation.pop('parent')
        return representation


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class ProductAllSizesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllSizes
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # user = serializers.ReadOnlyField(source='user.email')
    images = ProductImageSerializers(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        # all_sizes_data = validated_data.get("sizes")
        product = Product.objects.create(**validated_data)
        for image in images_data.getlist('images'):
            Image.objects.create(product=product, image=image)
        # for size in all_sizes_data:
        #     AllSizes.object.create(product=product, value=size["value"], price=size["price"],
        #                            in_stock=size["in_stock"], currency=size["currency"])
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_result = 0
        representation['reviews'] = instance.comment.count()
        representation['likes'] = instance.like.filter(like=True).count()
        representation['sizes'] = ProductAllSizesSerializer(instance.all_sizes.all(), many=True).data
        for i in instance.rating.all():
            rating_result += int(i.rating)
        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation['rating'] = rating_result / instance.rating.all().count()
        representation["images"] = ImageSerializer(instance.images.all(), many=True).data

        return representation


class Review2Serializers(serializers.ModelSerializer):

    class Meta:
        model = Review2
        fields = ('rating', )


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор отзывов
    """
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Review
        fields = '__all__'


class RetriveReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детального отзыва
    """
    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_result = 0
        representation['likes'] = instance.like.filter(like=True).count()
        representation['sizes'] = ProductAllSizesSerializer(instance.all_sizes.all(), many=True).data
        for i in instance.rating.all():
            rating_result += int(i.rating)
        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation['rating'] = rating_result / instance.rating.all().count()
        representation["images"] = ImageSerializer(instance.images.all(), many=True).data
        representation['reviews'] = ReviewSerializer(instance.comment.all(), many=True).data
        representation['colors'] = ProductSerializer(instance.children.all(), many=True).data
        return representation


class FavouriteProductSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = FavouriteProduct
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        product = validated_data.get('product')

        if FavouriteProduct.objects.filter(user=user, product=product):
            return FavouriteProduct.objects.get(user=user, product=product)
        else:
            return FavouriteProduct.objects.create(user=user, product=product)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

