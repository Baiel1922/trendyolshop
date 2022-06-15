from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.TextField()
    slug = models.SlugField(max_length=100, unique=True, primary_key=True)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    filter_f = models.CharField(max_length=550)
    def __str__(self):
        if not self.parent:
            return self.slug
        else:
            return f'{self.parent} --> {self.slug}'

    def save(self, *args, **kwargs):
        # self.slug = self.title.lower()
        self.filter_f = f"{self.parent}-{self.slug}"
        super(Category, self).save(*args, **kwargs)

class Color(models.Model):
    color = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, primary_key=True, default="")

    class Meta:
        verbose_name = 'Color'
        verbose_name_plural = 'Colors'


class Brand(models.Model):
    brand = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, primary_key=True, default='brand')

    class Meta:
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands'

    def __str__(self):
        return self.brand



class SizeL(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, primary_key=True, default='sizel')

    class Meta:
        verbose_name = 'SizeL'
        verbose_name_plural = 'SizeLs'

class Product(models.Model):
    CHOICES = (
        ('in stock', 'В наличии'),
        ('in out stock', 'Нет в наличии')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    parent = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    link = models.TextField()
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name='products')
    discounted_price = models.PositiveIntegerField(blank=True, null=True)
    selling_price = models.PositiveIntegerField()
    original_price = models.PositiveIntegerField()
    show_size = models.ForeignKey(SizeL, on_delete=models.CASCADE, related_name='sizes')
    campaign = models.CharField(max_length=255)
    currency = models.CharField(max_length=55)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

class AllSizes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sizes', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='all_sizes')
    value = models.ForeignKey(SizeL, on_delete=models.CASCADE, related_name='all_sizes')
    in_stock = models.BooleanField(default=False)
    price = models.PositiveIntegerField()
    currency = models.CharField(max_length=50)
    class Meta:
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'


class Review2(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    name = models.CharField(max_length=100, null=True, blank=True)
    comment = models.TextField(blank=True, null=True)
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ])

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'

    # def __str__(self):
    #     return self.rating


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', null=True, blank=True)
    image = models.ImageField(upload_to='images', max_length=1000)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'

    # def __str__(self):
    #     return self.product


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    comment = models.TextField()

    def __str__(self):
        return f'{self.user} - {self.comment}'

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class FavouriteProduct(models.Model):
    """
    Моделька избранных
    """
    user = models.ForeignKey(User, related_name='favourite', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='favourite', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Favourite'
        verbose_name_plural = 'Favourites'


class Like(models.Model):
    """
    Модель Лайков
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='like')
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.like}'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


        verbose_name = 'Like'
        verbose_name_plural = 'Likes'
