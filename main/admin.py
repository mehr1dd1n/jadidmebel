from django.contrib import admin
from .models import Category, Product, Portfolio, Review, Order, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'name_ru', 'name_en', 'slug', 'order']
    prepopulated_fields = {'slug': ('name_uz',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name_uz', 'category', 'material', 'price', 'is_featured', 'is_active']
    list_filter = ['category', 'material', 'is_featured', 'is_active']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title_uz', 'is_active', 'created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_active', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'product', 'status', 'created_at']
    list_filter = ['status']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    pass
