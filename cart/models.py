from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product, AllSizes
User = get_user_model()
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to="profile_images", null=True, blank=True)
    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.email


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.ForeignKey(AllSizes, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name

    def add_amount(self):
        amount = self.product.selling_price * self.quantity
        profile = self.user.profile
        profile.total_price = profile.total_price + amount
        profile.save()
        return True