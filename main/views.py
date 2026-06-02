from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category, Portfolio, Review, Order, SiteSettings


def get_site_settings():
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    return settings_obj


def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.all()
    reviews = Review.objects.filter(is_active=True)[:6]
    settings_obj = get_site_settings()
    return render(request, 'home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'reviews': reviews,
        'settings': settings_obj,
        'page': 'home',
    })


def products(request):
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    material = request.GET.get('material')

    qs = Product.objects.filter(is_active=True)
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        qs = qs.filter(category=active_category)

    if material:
        qs = qs.filter(material=material)

    settings_obj = get_site_settings()
    return render(request, 'products.html', {
        'products': qs,
        'categories': categories,
        'active_category': active_category,
        'active_material': material,
        'settings': settings_obj,
        'page': 'products',
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=pk)[:4]
    settings_obj = get_site_settings()
    return render(request, 'product_detail.html', {
        'product': product,
        'related': related,
        'settings': settings_obj,
        'page': 'products',
    })


def portfolio(request):
    works = Portfolio.objects.filter(is_active=True)
    settings_obj = get_site_settings()
    return render(request, 'portfolio.html', {
        'works': works,
        'settings': settings_obj,
        'page': 'portfolio',
    })


def about(request):
    settings_obj = get_site_settings()
    return render(request, 'about.html', {
        'settings': settings_obj,
        'page': 'about',
    })


def contact(request):
    settings_obj = get_site_settings()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and phone:
            Order.objects.create(name=name, phone=phone, message=message_text)
            messages.success(request, "✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog'lanamiz.")
            return redirect('contact')
        else:
            messages.error(request, "❌ Ism va telefon raqamni to'ldiring.")

    return render(request, 'contact.html', {
        'settings': settings_obj,
        'page': 'contact',
    })


def order_product(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    settings_obj = get_site_settings()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        phone = request.POST.get('phone', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and phone:
            Order.objects.create(product=product, name=name, phone=phone, message=message_text)
            messages.success(request, "✅ Buyurtmangiz qabul qilindi! Tez orada siz bilan bog'lanamiz.")
            return redirect('products')
        else:
            messages.error(request, "❌ Ma'lumotlarni to'ldiring.")

    return render(request, 'order_modal.html', {
        'product': product,
        'settings': settings_obj,
    })