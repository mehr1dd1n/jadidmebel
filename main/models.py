from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Kategoriya nomi")
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, default='🪑', verbose_name="Emoji belgisi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order']

    def __str__(self):
        return self.name


class Product(models.Model):
    MATERIAL_CHOICES = [
        ('yogoch', "Yog'och"),
        ('mdf', 'MDF'),
        ('metall', 'Metall'),
        ('shisha', 'Shisha'),
        ('kombinatsiya', 'Kombinatsiya'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Kategoriya")
    name = models.CharField(max_length=200, verbose_name="Mahsulot nomi")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, default='yogoch', verbose_name="Material")
    color = models.CharField(max_length=100, blank=True, verbose_name="Rang")
    price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Narx (so'm)")
    image = models.ImageField(upload_to='products/', verbose_name="Rasm")
    is_featured = models.BooleanField(default=False, verbose_name="Asosiy sahifada ko'rsatish")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_price_display(self):
        if self.price:
            return f"{int(self.price):,} so'm".replace(',', ' ')
        return "Narx so'rash"


class Portfolio(models.Model):
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    image = models.ImageField(upload_to='portfolio/', verbose_name="Rasm")
    before_image = models.ImageField(upload_to='portfolio/before/', blank=True, null=True, verbose_name="Oldin (ixtiyoriy)")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolio ishlari"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Review(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ism")
    text = models.TextField(verbose_name="Fikr")
    rating = models.PositiveIntegerField(default=5, verbose_name="Baho (1-5)")
    avatar = models.ImageField(upload_to='reviews/', blank=True, null=True, verbose_name="Rasm (ixtiyoriy)")
    is_active = models.BooleanField(default=True, verbose_name="Ko'rsatish")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mijoz fikri"
        verbose_name_plural = "Mijozlar fikrlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.rating}⭐"


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('processing', 'Ko\'rib chiqilmoqda'),
        ('done', 'Bajarildi'),
        ('cancelled', 'Bekor qilindi'),
    ]

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Mahsulot")
    name = models.CharField(max_length=100, verbose_name="Ism")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    message = models.TextField(blank=True, verbose_name="Xabar")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holat")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.phone} ({self.get_status_display()})"


class SiteSettings(models.Model):
    phone = models.CharField(max_length=20, default='+998901234567', verbose_name="Telefon")
    telegram = models.CharField(max_length=100, default='https://t.me/jadidmebel', verbose_name="Telegram link")
    whatsapp = models.CharField(max_length=20, default='+998901234567', verbose_name="WhatsApp raqam")
    address = models.CharField(max_length=300, default="Toshkent sh., Yunusobod tumani", verbose_name="Manzil")
    instagram = models.CharField(max_length=200, blank=True, verbose_name="Instagram link")
    about_text = models.TextField(default="Jadid Mebel — 2018-yildan beri Toshkentda sifatli mebel ishlab chiqarmoqda.", verbose_name="Biz haqimizda matni")
    map_embed = models.TextField(blank=True, verbose_name="Google Maps iframe kodi")

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"