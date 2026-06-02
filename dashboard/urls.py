from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),

    # Products
    path('mahsulotlar/', views.product_list, name='dashboard_product_list'),
    path('mahsulotlar/qoshish/', views.product_add, name='dashboard_product_add'),
    path('mahsulotlar/<int:pk>/tahrirlash/', views.product_edit, name='dashboard_product_edit'),
    path('mahsulotlar/<int:pk>/ochirish/', views.product_delete, name='dashboard_product_delete'),

    # Categories
    path('kategoriyalar/', views.category_list, name='dashboard_category_list'),
    path('kategoriyalar/qoshish/', views.category_add, name='dashboard_category_add'),
    path('kategoriyalar/<int:pk>/tahrirlash/', views.category_edit, name='dashboard_category_edit'),
    path('kategoriyalar/<int:pk>/ochirish/', views.category_delete, name='dashboard_category_delete'),

    # Portfolio
    path('portfolio/', views.portfolio_list, name='dashboard_portfolio_list'),
    path('portfolio/qoshish/', views.portfolio_add, name='dashboard_portfolio_add'),
    path('portfolio/<int:pk>/tahrirlash/', views.portfolio_edit, name='dashboard_portfolio_edit'),
    path('portfolio/<int:pk>/ochirish/', views.portfolio_delete, name='dashboard_portfolio_delete'),

    # Orders
    path('buyurtmalar/', views.order_list, name='dashboard_order_list'),
    path('buyurtmalar/<int:pk>/holat/', views.order_update_status, name='dashboard_order_update_status'),
    path('buyurtmalar/<int:pk>/ochirish/', views.order_delete, name='dashboard_order_delete'),

    # Reviews
    path('fikrlar/', views.review_list, name='dashboard_review_list'),
    path('fikrlar/qoshish/', views.review_add, name='dashboard_review_add'),
    path('fikrlar/<int:pk>/ochirish/', views.review_delete, name='dashboard_review_delete'),

    # Settings
    path('sozlamalar/', views.site_settings, name='dashboard_settings'),
]