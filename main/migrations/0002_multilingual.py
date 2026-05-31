from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(model_name='category', old_name='name', new_name='name_uz'),
        migrations.AddField(model_name='category', name='name_ru', field=models.CharField(blank=True, max_length=100, verbose_name='Nomi (Rus)')),
        migrations.AddField(model_name='category', name='name_en', field=models.CharField(blank=True, max_length=100, verbose_name='Nomi (Ingliz)')),
        migrations.RenameField(model_name='product', old_name='name', new_name='name_uz'),
        migrations.RenameField(model_name='product', old_name='description', new_name='description_uz'),
        migrations.RenameField(model_name='product', old_name='color', new_name='color_uz'),
        migrations.AddField(model_name='product', name='name_ru', field=models.CharField(blank=True, max_length=200, verbose_name='Nomi (Rus)')),
        migrations.AddField(model_name='product', name='name_en', field=models.CharField(blank=True, max_length=200, verbose_name='Nomi (Ingliz)')),
        migrations.AddField(model_name='product', name='description_ru', field=models.TextField(blank=True, verbose_name='Tavsif (Rus)')),
        migrations.AddField(model_name='product', name='description_en', field=models.TextField(blank=True, verbose_name='Tavsif (Ingliz)')),
        migrations.AddField(model_name='product', name='color_ru', field=models.CharField(blank=True, max_length=100, verbose_name='Rang (Rus)')),
        migrations.AddField(model_name='product', name='color_en', field=models.CharField(blank=True, max_length=100, verbose_name='Rang (Ingliz)')),
        migrations.RenameField(model_name='portfolio', old_name='title', new_name='title_uz'),
        migrations.RenameField(model_name='portfolio', old_name='description', new_name='description_uz'),
        migrations.AddField(model_name='portfolio', name='title_ru', field=models.CharField(blank=True, max_length=200, verbose_name='Sarlavha (Rus)')),
        migrations.AddField(model_name='portfolio', name='title_en', field=models.CharField(blank=True, max_length=200, verbose_name='Sarlavha (Ingliz)')),
        migrations.AddField(model_name='portfolio', name='description_ru', field=models.TextField(blank=True, verbose_name='Tavsif (Rus)')),
        migrations.AddField(model_name='portfolio', name='description_en', field=models.TextField(blank=True, verbose_name='Tavsif (Ingliz)')),
        migrations.RenameField(model_name='sitesettings', old_name='about_text', new_name='about_text_uz'),
        migrations.RenameField(model_name='sitesettings', old_name='address', new_name='address_uz'),
        migrations.AddField(model_name='sitesettings', name='about_text_ru', field=models.TextField(blank=True, verbose_name='Biz haqimizda (Rus)')),
        migrations.AddField(model_name='sitesettings', name='about_text_en', field=models.TextField(blank=True, verbose_name='Biz haqimizda (Ingliz)')),
        migrations.AddField(model_name='sitesettings', name='address_ru', field=models.CharField(blank=True, max_length=300, verbose_name='Manzil (Rus)')),
        migrations.AddField(model_name='sitesettings', name='address_en', field=models.CharField(blank=True, max_length=300, verbose_name='Manzil (Ingliz)')),
    ]
