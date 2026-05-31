from django.db import models
from main.i18n_utils import get_lang
from main.translations import translate


class TranslatableMixin:
    def get_t(self, field):
        lang = get_lang()
        for code in (lang, 'uz', 'ru', 'en'):
            val = getattr(self, f'{field}_{code}', None)
            if val:
                return val
        return ''


class Category(TranslatableMixin, models.Model):
    name_uz = models.CharField(max_length=100, verbose_name="Nomi (O'zbek)")
    name_ru = models.CharField(max_length=100, blank=True, verbose_name='Nomi (Rus)')
    name_en = models.CharField(max_length=100, blank=True, verbose_name='Nomi (Ingliz)')
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, default='🪑', verbose_name="Emoji belgisi")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order']

    def __str__(self):
        return self.name_uz


class Product(TranslatableMixin, models.Model):
    MATERIAL_CHOICES = [
        ('yogoch', "yogoch"),
        ('mdf', 'mdf'),
        ('metall', 'metall'),
        ('shisha', 'shisha'),
        ('kombinatsiya', 'kombinatsiya'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Kategoriya")
    name_uz = models.CharField(max_length=200, verbose_name="Nomi (O'zbek)")
    name_ru = models.CharField(max_length=200, blank=True, verbose_name='Nomi (Rus)')
    name_en = models.CharField(max_length=200, blank=True, verbose_name='Nomi (Ingliz)')
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (O'zbek)")
    description_ru = models.TextField(blank=True, verbose_name='Tavsif (Rus)')
    description_en = models.TextField(blank=True, verbose_name='Tavsif (Ingliz)')
    material = models.CharField(max_length=50, choices=MATERIAL_CHOICES, default='yogoch', verbose_name="Material")
    color_uz = models.CharField(max_length=100, blank=True, verbose_name="Rang (O'zbek)")
    color_ru = models.CharField(max_length=100, blank=True, verbose_name='Rang (Rus)')
    color_en = models.CharField(max_length=100, blank=True, verbose_name='Rang (Ingliz)')
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
        return self.name_uz

    def get_material_display(self):
        return translate(f'mat.{self.material}')

    def get_price_display(self):
        if self.price:
            amount = f"{int(self.price):,}".replace(',', ' ')
            suffix = {'uz': "so'm", 'ru': 'сум', 'en': 'UZS'}.get(get_lang(), "so'm")
            return f"{amount} {suffix}"
        return translate('common.price_ask')


class Portfolio(TranslatableMixin, models.Model):
    title_uz = models.CharField(max_length=200, verbose_name="Sarlavha (O'zbek)")
    title_ru = models.CharField(max_length=200, blank=True, verbose_name='Sarlavha (Rus)')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Sarlavha (Ingliz)')
    description_uz = models.TextField(blank=True, verbose_name="Tavsif (O'zbek)")
    description_ru = models.TextField(blank=True, verbose_name='Tavsif (Rus)')
    description_en = models.TextField(blank=True, verbose_name='Tavsif (Ingliz)')
    image = models.ImageField(upload_to='portfolio/', verbose_name="Rasm")
    before_image = models.ImageField(upload_to='portfolio/before/', blank=True, null=True, verbose_name="Oldin (ixtiyoriy)")
    is_active = models.BooleanField(default=True, verbose_name="Faol")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Portfolio"
        verbose_name_plural = "Portfolio ishlari"
        ordering = ['-created_at']

    def __str__(self):
        return self.title_uz


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


class SiteSettings(TranslatableMixin, models.Model):
    phone = models.CharField(max_length=20, default='+998901234567', verbose_name="Telefon")
    telegram = models.CharField(max_length=100, default='https://t.me/jadidmebel', verbose_name="Telegram link")
    whatsapp = models.CharField(max_length=20, default='+998901234567', verbose_name="WhatsApp raqam")
    address_uz = models.CharField(max_length=300, default="Toshkent sh., Yunusobod tumani", verbose_name="Manzil (O'zbek)")
    address_ru = models.CharField(max_length=300, blank=True, verbose_name='Manzil (Rus)')
    address_en = models.CharField(max_length=300, blank=True, verbose_name='Manzil (Ingliz)')
    instagram = models.CharField(max_length=200, blank=True, verbose_name="Instagram link")
    about_text_uz = models.TextField(
        default="Jadid Mebel — 2018-yildan beri Toshkentda sifatli mebel ishlab chiqarmoqda.",
        verbose_name="Biz haqimizda (O'zbek)",
    )
    about_text_ru = models.TextField(blank=True, verbose_name='Biz haqimizda (Rus)')
    about_text_en = models.TextField(blank=True, verbose_name='Biz haqimizda (Ingliz)')
    map_embed = models.TextField(blank=True, verbose_name="Google Maps iframe kodi")

    class Meta:
        verbose_name = "Sayt sozlamalari"
        verbose_name_plural = "Sayt sozlamalari"

    def __str__(self):
        return "Sayt sozlamalari"
