def fill_product(post, product):
    product.name_uz = post.get('name_uz', '').strip()
    product.name_ru = post.get('name_ru', '').strip()
    product.name_en = post.get('name_en', '').strip()
    product.description_uz = post.get('description_uz', '').strip()
    product.description_ru = post.get('description_ru', '').strip()
    product.description_en = post.get('description_en', '').strip()
    product.color_uz = post.get('color_uz', '').strip()
    product.color_ru = post.get('color_ru', '').strip()
    product.color_en = post.get('color_en', '').strip()
    product.material = post.get('material', 'yogoch')
    product.category_id = post['category']
    product.is_featured = bool(post.get('is_featured'))
    product.is_active = bool(post.get('is_active', True))


def fill_category(post, category):
    category.name_uz = post.get('name_uz', '').strip()
    category.name_ru = post.get('name_ru', '').strip()
    category.name_en = post.get('name_en', '').strip()
    category.slug = post.get('slug', '').strip()
    category.icon = post.get('icon', '🪑')
    category.order = post.get('order', 0) or 0


def fill_portfolio(post, work):
    work.title_uz = post.get('title_uz', '').strip()
    work.title_ru = post.get('title_ru', '').strip()
    work.title_en = post.get('title_en', '').strip()
    work.description_uz = post.get('description_uz', '').strip()
    work.description_ru = post.get('description_ru', '').strip()
    work.description_en = post.get('description_en', '').strip()
    work.is_active = bool(post.get('is_active', True))


def fill_settings(post, settings_obj):
    settings_obj.phone = post.get('phone', settings_obj.phone)
    settings_obj.telegram = post.get('telegram', settings_obj.telegram)
    settings_obj.whatsapp = post.get('whatsapp', settings_obj.whatsapp)
    settings_obj.instagram = post.get('instagram', settings_obj.instagram)
    settings_obj.about_text_uz = post.get('about_text_uz', settings_obj.about_text_uz)
    settings_obj.about_text_ru = post.get('about_text_ru', '')
    settings_obj.about_text_en = post.get('about_text_en', '')
    settings_obj.address_uz = post.get('address_uz', settings_obj.address_uz)
    settings_obj.address_ru = post.get('address_ru', '')
    settings_obj.address_en = post.get('address_en', '')
    settings_obj.map_embed = post.get('map_embed', settings_obj.map_embed)
