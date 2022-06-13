from django.contrib import admin

from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ['title', ]


class ColorAdmin(admin.ModelAdmin):
    list_display = ('color', 'slug')
    list_display_links = ('color', 'slug')
    search_fields = ('color', )


class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand', 'slug')
    list_display_links = ('brand', 'slug')
    search_fields = ['brand', ]


class SizeLAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_display_links = ('name', 'slug')
    search_fields = ['name', ]


class AllSizesAdmin(admin.ModelAdmin):
    list_display = ('product', 'value', 'price',)
    list_display_link = ('product', 'value', 'price',)
    search_fields = ['product', ]


class Review2Admin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating')
    list_display_link = ('user', 'product', 'rating')
    search_fields = ['user', 'rating',]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'comment')
    list_display_link = ('user', 'product', 'comment')
    search_fields = ['user', 'comment']


class FavouriteProductAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'date')
    list_display_link = ('user', 'product', 'date')
    search_fields = ['user', 'product']


class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'like')
    list_display_link = ('user', 'product', 'like')
    search_fields = ['user', 'product']


class SizeInProduct(admin.TabularInline):
    model = AllSizes
    fields = ()
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'selling_price', )
    list_display_links = ('name', 'category', 'brand', 'selling_price', )
    search_fields = ['name', 'brand', ]
    list_filter = ('category', 'brand', 'selling_price')
    inlines = [
        SizeInProduct
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Review2, Review2Admin)
admin.site.register(SizeL, SizeLAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FavouriteProduct, FavouriteProductAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Image,)
admin.site.register(AllSizes, AllSizesAdmin)