from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count
from main.models import Product, Category, Portfolio, Review, Order, SiteSettings


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, "Login yoki parol noto'g'ri!")

    return render(request, 'dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


@login_required
def dashboard_home(request):
    context = {
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),
        'new_orders': Order.objects.filter(status='new').count(),
        'total_portfolio': Portfolio.objects.count(),
        'recent_orders': Order.objects.select_related('product').order_by('-created_at')[:8],
        'categories': Category.objects.annotate(product_count=Count('products')),
    }
    return render(request, 'dashboard/home.html', context)


# ─── PRODUCTS ───────────────────────────────────────────────
@login_required
def product_list(request):
    category_id = request.GET.get('category')
    qs = Product.objects.select_related('category').order_by('-created_at')
    if category_id:
        qs = qs.filter(category_id=category_id)
    return render(request, 'dashboard/product_list.html', {
        'products': qs,
        'categories': Category.objects.all(),
        'active_category': category_id,
    })


@login_required
def product_add(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            product = Product(
                name=request.POST['name'],
                description=request.POST.get('description', ''),
                material=request.POST.get('material', 'yogoch'),
                color=request.POST.get('color', ''),
                category_id=request.POST['category'],
                is_featured=bool(request.POST.get('is_featured')),
                is_active=bool(request.POST.get('is_active', True)),
            )
            price = request.POST.get('price')
            if price:
                product.price = int(price)
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            messages.success(request, f"✅ '{product.name}' mahsuloti qo'shildi!")
            return redirect('dashboard_product_list')
        except Exception as e:
            messages.error(request, f"❌ Xatolik: {e}")
    return render(request, 'dashboard/product_form.html', {'categories': categories, 'action': 'Qo\'shish'})


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    if request.method == 'POST':
        try:
            product.name = request.POST['name']
            product.description = request.POST.get('description', '')
            product.material = request.POST.get('material', 'yogoch')
            product.color = request.POST.get('color', '')
            product.category_id = request.POST['category']
            product.is_featured = bool(request.POST.get('is_featured'))
            product.is_active = bool(request.POST.get('is_active'))
            price = request.POST.get('price')
            product.price = int(price) if price else None
            if 'image' in request.FILES:
                product.image = request.FILES['image']
            product.save()
            messages.success(request, f"✅ '{product.name}' tahrirlandi!")
            return redirect('dashboard_product_list')
        except Exception as e:
            messages.error(request, f"❌ Xatolik: {e}")
    return render(request, 'dashboard/product_form.html', {
        'product': product, 'categories': categories, 'action': 'Tahrirlash'
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"🗑️ '{name}' o'chirildi.")
        return redirect('dashboard_product_list')
    return render(request, 'dashboard/confirm_delete.html', {'obj': product, 'type': 'Mahsulot'})


# ─── CATEGORIES ─────────────────────────────────────────────
@login_required
def category_list(request):
    categories = Category.objects.annotate(product_count=Count('products'))
    return render(request, 'dashboard/category_list.html', {'categories': categories})


@login_required
def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        slug = request.POST.get('slug', '').strip()
        icon = request.POST.get('icon', '🪑')
        order = request.POST.get('order', 0)
        if name and slug:
            Category.objects.create(name=name, slug=slug, icon=icon, order=order)
            messages.success(request, f"✅ '{name}' kategoriyasi qo'shildi!")
            return redirect('dashboard_category_list')
        messages.error(request, "Nom va slug kiritish shart!")
    return render(request, 'dashboard/category_form.html', {'action': "Qo'shish"})


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.slug = request.POST.get('slug', category.slug)
        category.icon = request.POST.get('icon', category.icon)
        category.order = request.POST.get('order', category.order)
        category.save()
        messages.success(request, "✅ Kategoriya tahrirlandi!")
        return redirect('dashboard_category_list')
    return render(request, 'dashboard/category_form.html', {'category': category, 'action': 'Tahrirlash'})


@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "🗑️ Kategoriya o'chirildi.")
        return redirect('dashboard_category_list')
    return render(request, 'dashboard/confirm_delete.html', {'obj': category, 'type': 'Kategoriya'})


# ─── PORTFOLIO ──────────────────────────────────────────────
@login_required
def portfolio_list(request):
    works = Portfolio.objects.order_by('-created_at')
    return render(request, 'dashboard/portfolio_list.html', {'works': works})


@login_required
def portfolio_add(request):
    if request.method == 'POST':
        try:
            work = Portfolio(
                title=request.POST['title'],
                description=request.POST.get('description', ''),
                is_active=bool(request.POST.get('is_active', True)),
            )
            if 'image' in request.FILES:
                work.image = request.FILES['image']
            if 'before_image' in request.FILES:
                work.before_image = request.FILES['before_image']
            work.save()
            messages.success(request, "✅ Portfolio ishi qo'shildi!")
            return redirect('dashboard_portfolio_list')
        except Exception as e:
            messages.error(request, f"❌ Xatolik: {e}")
    return render(request, 'dashboard/portfolio_form.html', {'action': "Qo'shish"})


@login_required
def portfolio_edit(request, pk):
    work = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        work.title = request.POST.get('title', work.title)
        work.description = request.POST.get('description', '')
        work.is_active = bool(request.POST.get('is_active'))
        if 'image' in request.FILES:
            work.image = request.FILES['image']
        if 'before_image' in request.FILES:
            work.before_image = request.FILES['before_image']
        work.save()
        messages.success(request, "✅ Portfolio tahrirlandi!")
        return redirect('dashboard_portfolio_list')
    return render(request, 'dashboard/portfolio_form.html', {'work': work, 'action': 'Tahrirlash'})


@login_required
def portfolio_delete(request, pk):
    work = get_object_or_404(Portfolio, pk=pk)
    if request.method == 'POST':
        work.delete()
        messages.success(request, "🗑️ Portfolio ishi o'chirildi.")
        return redirect('dashboard_portfolio_list')
    return render(request, 'dashboard/confirm_delete.html', {'obj': work, 'type': 'Portfolio'})


# ─── ORDERS ─────────────────────────────────────────────────
@login_required
def order_list(request):
    status = request.GET.get('status')
    qs = Order.objects.select_related('product').order_by('-created_at')
    if status:
        qs = qs.filter(status=status)
    return render(request, 'dashboard/order_list.html', {
        'orders': qs,
        'active_status': status,
        'status_choices': Order.STATUS_CHOICES,
    })


@login_required
def order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = request.POST.get('status', order.status)
        order.save()
        messages.success(request, "✅ Holat yangilandi!")
    return redirect('dashboard_order_list')


@login_required
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "🗑️ Buyurtma o'chirildi.")
    return redirect('dashboard_order_list')


# ─── REVIEWS ────────────────────────────────────────────────
@login_required
def review_list(request):
    reviews = Review.objects.order_by('-created_at')
    return render(request, 'dashboard/review_list.html', {'reviews': reviews})


@login_required
def review_add(request):
    if request.method == 'POST':
        review = Review(
            name=request.POST['name'],
            text=request.POST['text'],
            rating=int(request.POST.get('rating', 5)),
            is_active=bool(request.POST.get('is_active', True)),
        )
        if 'avatar' in request.FILES:
            review.avatar = request.FILES['avatar']
        review.save()
        messages.success(request, "✅ Fikr qo'shildi!")
        return redirect('dashboard_review_list')
    return render(request, 'dashboard/review_form.html', {'action': "Qo'shish"})


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, "🗑️ Fikr o'chirildi.")
    return redirect('dashboard_review_list')


# ─── SETTINGS ───────────────────────────────────────────────
@login_required
def site_settings(request):
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    if request.method == 'POST':
        settings_obj.phone = request.POST.get('phone', settings_obj.phone)
        settings_obj.telegram = request.POST.get('telegram', settings_obj.telegram)
        settings_obj.whatsapp = request.POST.get('whatsapp', settings_obj.whatsapp)
        settings_obj.address = request.POST.get('address', settings_obj.address)
        settings_obj.instagram = request.POST.get('instagram', settings_obj.instagram)
        settings_obj.about_text = request.POST.get('about_text', settings_obj.about_text)
        settings_obj.map_embed = request.POST.get('map_embed', settings_obj.map_embed)
        settings_obj.save()
        messages.success(request, "✅ Sozlamalar saqlandi!")
        return redirect('dashboard_settings')
    return render(request, 'dashboard/settings.html', {'settings': settings_obj})