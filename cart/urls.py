from django.urls import path, include
from rest_framework import routers
from . import views


urlpatterns = [
    path('list/', views.CartItemView.as_view(), name="cart"),
    path('add/', views.CartItemAddView.as_view()),
    path('delete/<int:pk>/', views.CartItemDelView.as_view()),
    path('add_one/<int:pk>/', views.CartItemAddOneView.as_view()),
    path('reduce_one/<int:pk>/', views.CartItemReduceOneView.as_view()),
]