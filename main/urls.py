from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mahsulotlar/', views.products, name='products'),
    path('mahsulotlar/<int:pk>/', views.product_detail, name='product_detail'),
    path('mahsulotlar/<int:pk>/buyurtma/', views.order_product, name='order_product'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('biz-haqimizda/', views.about, name='about'),
    path('aloqa/', views.contact, name='contact'),
]