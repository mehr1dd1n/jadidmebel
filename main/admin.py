from django.contrib import admin
from .models import Category, Product, Portfolio, Review, Order, SiteSettings


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'material', 'price', 'is_featured', 'is_active']
    list_filter = ['category', 'material', 'is_featured', 'is_active']
    list_editable = ['is_featured', 'is_active']


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_active', 'created_at']
    list_editable = ['is_active']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'product', 'status', 'created_at']
    list_filter = ['status']
    list_editable = ['status']


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    pass