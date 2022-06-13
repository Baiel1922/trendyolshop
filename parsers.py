from product.models import *
from trendyol_scraper import TrendyolScraper
from time import time
import json
from django.db.utils import IntegrityError
import os.path

class Scraper:
    def __init__(self):
        pass

    def parse_colors(self):
        start_time = time()
        Color.objects.all().delete()
        scraper = TrendyolScraper()
        colors = scraper.get_all_colors(write2file=True)
        with open('output/colors.json') as f:
            colors_json = json.load(f)
        for color in colors_json:
            print(color)
            name = color['name']
            slug = color['slug']
            Color.objects.update_or_create(slug=slug, defaults={"color": name})
        print(len(colors))
        print(time() - start_time)
        return f'colors were added successfully! {len(colors)}'

    def parse_brands(self):
        start_time = time()
        Brand.objects.all().delete()
        scraper = TrendyolScraper()
        brands = scraper.get_all_brands(write2file=True)
        with open('output/brands.json') as f:
            brands_json = json.load(f)
        for brand in brands_json:
            name = brand['name']
            slug = brand['slug']
            Brand.objects.update_or_create(slug=slug, defaults={'brand': name})
        print(time() - start_time)
        return f'brands were added successfully {len(brands)}'

    def parse_sizes(self):
        start_time = time()
        SizeL.objects.all().delete()
        scraper = TrendyolScraper()
        sizes = scraper.get_all_sizes(write2file=True)
        with open('output/sizes.json') as f:
            sizes_json = json.load(f)
        for size in sizes_json:
            name = size['name']
            slug = size['slug']
            SizeL.objects.update_or_create(slug=slug, defaults={"name": name})
        print(len(sizes))
        print(time() - start_time)
        return f'sizes added successfully! {len(sizes)}'

    def parse_categories(self):
        start_time = time()
        scraper = TrendyolScraper()
        all_categories = scraper.get_all_categories(write2file=True)
        with open('output/categories.json') as f:
            categories_json = json.load(f)
        Category.objects.all().delete()
        for category in categories_json:
            name = category['name']
            slug = category['slug']
            try:
                parent = category['parent']
                parent = Category.objects.get(slug=parent)
                Category.objects.update_or_create(slug=slug, defaults={'title': name, 'parent': parent})
            except:
                Category.objects.update_or_create(slug=slug, defaults={'title': name})
        print(len(all_categories))
        print(time() - start_time)
        return f'Categories were added sucessfully! {len(all_categories)}'


    def parse_products(self, coefficient):
        start_time = time()
        Product.objects.all().delete()
        count_all_products = 0
        count_category = 0
        count_not_added_products = 0
        count_size = 0
        count_brand = 0
        count_color = 0
        count_added_products = 0
        count_product_size = 0
        scraper = TrendyolScraper()
        all_products = scraper.get_all_products(write2file=True)
        with open('output/products.json') as f:
            products_json = json.load(f)
        for product in products_json:
            id = product["id"]
            name = product["name"]
            link = product["link"]
            campaign = product["campaign"]
            discounted_price = product["price"]["discountedPrice"]["value"]
            selling_price = product["price"]["sellingPrice"]["value"]
            original_price = product["price"]["originalPrice"]["value"]
            currency = product["price"]["currency"]
            description = product["description"]
            brand_slug = product["brand"]["slug"]
            try:
                brand = Brand.objects.get(slug=brand_slug)
            except:
                Brand.objects.create(slug=brand_slug, brand=brand_slug)
                brand = Brand.objects.get(slug=brand_slug)
                count_brand += 1
            color_slug = product["showColor"]
            try:
                color = Color.objects.get(slug=color_slug)
            except:
                Color.objects.create(slug=color_slug, color=color_slug)
                color = Color.objects.get(slug=color_slug)
                count_color += 1
            category_slug = product["category"]["slug"]
            try:
                category = Category.objects.get(slug=category_slug)
            except:
                Category.objects.create(slug=category_slug, title=category_slug)
                category = Category.objects.get(slug=category_slug)
                count_category += 1
            show_size_slug = product["showSize"].lower()
            try:
                show_size = SizeL.objects.get(slug=show_size_slug)
            except:
                SizeL.objects.create(slug=show_size_slug, name=show_size_slug.upper())
                show_size = SizeL.objects.get(slug=show_size_slug)
                count_size += 1
            try:
                Product.objects.create(id=id,
                                       name=name,
                                       link=link,
                                       description=description,
                                       category=category,
                                       discounted_price=discounted_price * coefficient,
                                       selling_price=selling_price * coefficient,
                                       original_price=original_price * coefficient,
                                       brand=brand,
                                       campaign=campaign,
                                       currency=currency,
                                       color=color,
                                       show_size=show_size)
                count_added_products += 1
            except IntegrityError:
                count_not_added_products += 1
            finally:
                count_all_products += 1
            all_sizes = product["sizes"]
            product_obj = Product.objects.get(pk=id)
            images_list = product['images']
            for image_url in images_list:
                Image.objects.get_or_create(product=product_obj, image=image_url)
                print('success!')
            # reviews = product["reviews"]
            # Rating.objects.filter(product=product_obj).delete()
            # for review in reviews:
            #     author = review["user"]
            #     rate = review["rate"]
            #     comment = review["comment"]
            #     date = review["date"]
            #     Rating.objects.create(product=product_obj,author=author, rating=rate, created_at=date, comment=comment)
            for size in all_sizes:
                value_slug = size["value"].lower()
                try:
                    value = SizeL.objects.get(slug=value_slug)
                except:
                    SizeL.objects.create(slug=value_slug, name=value.upper())
                    value = SizeL.objects.get(slug=value_slug)
                    count_product_size += 1
                in_stock = size["inStock"]
                price = size["price"]
                currency = size["currency"]
                AllSizes.objects.create(product=product_obj,
                                        value=value,
                                        in_stock=in_stock,
                                        price=price,
                                        currency=currency)
            colors = product['colors']
            for product_color in colors:
                id = product_color["product"]["id"]
                name = product_color["product"]["name"]
                link = product_color["product"]["link"]
                campaign = product_color["product"]["campaign"]
                discounted_price = product_color["product"]["price"]["discountedPrice"]["value"]
                selling_price = product_color["product"]["price"]["sellingPrice"]["value"]
                original_price = product_color["product"]["price"]["originalPrice"]["value"]
                currency = product_color["product"]["price"]["currency"]
                description = product_color["product"]["description"]
                brand_slug = product_color["product"]["brand"]["slug"]
                try:
                    brand = Brand.objects.get(slug=brand_slug)
                except:
                    Brand.objects.create(slug=brand_slug, brand=brand_slug)
                    brand = Brand.objects.get(slug=brand_slug)
                    count_brand += 1
                color_slug = product_color["slug"]
                try:
                    color = Color.objects.get(slug=color_slug)
                except:
                    Color.objects.create(slug=color_slug, color=color_slug)
                    color = Color.objects.get(slug=color_slug)
                    count_color += 1
                category_slug = product_color["product"]["category"]["slug"]
                try:
                    category = Category.objects.get(slug=category_slug)
                except:
                    Category.objects.create(slug=category_slug, title=category_slug)
                    category = Category.objects.get(slug=category_slug)
                    count_category += 1
                show_size_slug = product_color["product"]["showSize"].lower()
                try:
                    show_size = SizeL.objects.get(slug=show_size_slug)
                except:
                    SizeL.objects.create(slug=show_size_slug, name=show_size_slug.upper())
                    show_size = SizeL.objects.get(slug=show_size_slug)
                    count_size += 1
                try:
                    Product.objects.create(id=id,
                                           name=name,
                                           link=link,
                                           parent=product_obj,
                                           description=description,
                                           category=category,
                                           discounted_price=discounted_price * coefficient,
                                           selling_price=selling_price * coefficient,
                                           original_price=original_price * coefficient,
                                           brand=brand,
                                           campaign=campaign,
                                           currency=currency,
                                           color=color,
                                           show_size=show_size)
                    count_added_products += 1
                except IntegrityError:
                    count_not_added_products += 1
                finally:
                    count_all_products += 1
                all_sizes = product_color["product"]["sizes"]
                product_obj = Product.objects.get(pk=id)
                images_list2 = product_color["product"]["images"]
                for image_url in images_list:
                    Image.objects.get_or_create(product=product_obj, image=image_url)
                    print('success!')

                for size in all_sizes:
                    value_slug = size["value"].lower()
                    try:
                        value = SizeL.objects.get(slug=value_slug)
                    except:
                        SizeL.objects.create(slug=value_slug, name=value.upper())
                        value = SizeL.objects.get(slug=value_slug)
                        count_size += 1
                    in_stock = size["inStock"]
                    price = size["price"]
                    currency = size["currency"]
                    AllSizes.objects.create(product=product_obj,
                                            value=value,
                                            in_stock=in_stock,
                                            price=price,
                                            currency=currency)

        all_product_result = f"all products:, {count_all_products}"
        created_brands = f"{count_brand}: new brands were created"
        added_products = f"{count_added_products}: products were added"
        created_sizes = f"{count_size}:new sizes were created"
        created_category = f"{count_category}:categories were created"
        not_added_products = f"{count_not_added_products}: products with same id and they were not added"
        created_sizes_of_product = f"{count_product_size}: size of product were created"
        created_colors = f"{count_color}: colors were created"
        result_time = time() - start_time
        r_time = f"{result_time} seconds"
        return f"result: {r_time}, {all_product_result}, {added_products}, {not_added_products}, {created_brands}, {created_sizes}, {created_category}, {created_sizes_of_product}, {created_colors}"
