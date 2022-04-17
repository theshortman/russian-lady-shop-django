"""This script imports data from old database to the current database."""

import argparse
import os
import shutil
from collections import namedtuple
from random import choice

from django.conf import settings
from django.apps import apps
from django.db import connections
from django.core.files import File
from shop.settings import MEDIA_ROOT

CATEGORIES = [
    {'id': 1, 'name': 'Блузки и Жакеты',
     'description': 'В данной категории нашего интернет-магазина Вы можете найти блузки и жакеты российского и '
                    'белорусского производства. Доставка почтой наложенным платежом.',
     'slug': 'bluzki-i-jaketyi', 'sort': 1},
    {'id': 2, 'name': 'Юбки',
     'description': 'Наш интернет-магазин предлагаем Вам женские юбки от 50 до 58 размера. '
                    'Мы отправляем заказы почтой без предоплаты.',
     'slug': 'yubki', 'sort': 3},
    {'id': 3, 'name': 'Белорусские костюмы',
     'description': 'В данной категории нашего интернет-магазина Вы найдете женские костюмы белорусских производителей '
                    'от 50 до 58 размера. Мы отправляем заказы наложенным платежом.',
     'slug': 'belorusskie-kostyumyi', 'sort': 4},
    {'id': 4, 'name': 'Белорусские платья',
     'description': 'Данная категория нашего интернет-магазина содержит платья белорусского производства '
                    'для праздника и повседневной жизни. Мы отправляем заказы без предоплаты.',
     'slug': 'belorusskie-platya', 'sort': 5},
    {'id': 5, 'name': 'Российские платья',
     'description': 'В данной категории нашего интернет-магазина Вы можете найти платья от российских производителей. '
                    'Мы отправляем заказы наложенным платежом по всей России.',
     'slug': 'rossiyskie-platya', 'sort': 6},
    {'id': 6, 'name': 'Брюки',
     'description': 'В данной категории нашего интернет-магазина представлены женские брюки от 50 до 58 размера. '
                    'Мы отправляем заказы почтой без предоплаты.',
     'slug': 'bryuki', 'sort': 2},
    {'id': 7, 'name': 'Верхняя одежда',
     'description': 'В данной категории мы предлагаем Вам женские куртки, пальто и плащи от 50 до 58 размера '
                    'по приятным ценам без предоплаты.',
     'slug': 'verhnyaya-odejda', 'sort': 7}
]


def configure_app(old_db_name, old_db_user, old_db_password):
    conf = {
        'INSTALLED_APPS': [
            'catalog'
        ],
        'MEDIA_ROOT': MEDIA_ROOT,
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'db.sqlite3',
            },
            'old_db': {
                'NAME': old_db_name,
                'ENGINE': 'django.db.backends.mysql',
                'USER': old_db_user,
                'PASSWORD': old_db_password
            }
        }
    }

    settings.configure(**conf)
    apps.populate(settings.INSTALLED_APPS)


def namedtuple_fetchall(cursor):
    """Return all rows from a cursor as a namedtuple"""
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def parse_args():
    parser = argparse.ArgumentParser(
        description='Import data from old database to the current database.')
    parser.add_argument('old_db_name', type=str,
                        help='old database name')
    parser.add_argument('old_db_user', type=str,
                        help='old database user')
    parser.add_argument('old_db_password', type=str,
                        help='old database password')
    parser.add_argument('path_to_old_media', type=str,
                        help='path to old media files')

    return parser.parse_args()


def main():
    args = parse_args()

    configure_app(args.old_db_name, args.old_db_user, args.old_db_password)

    from catalog.models import Category, Product, ProductItem, ProductImage

    Category.objects.all().delete()
    Product.objects.all().delete()
    ProductItem.objects.all().delete()
    ProductImage.objects.all().delete()

    if os.path.exists(MEDIA_ROOT):
        shutil.rmtree(MEDIA_ROOT)
    os.mkdir(MEDIA_ROOT)

    for cat in CATEGORIES:
        Category(**cat).save()

    with connections['old_db'].cursor() as cursor:
        cursor.execute(
            "SELECT id, cat_id, name, slug, parameter AS detail, description, price FROM product")
        products = namedtuple_fetchall(cursor)

        products_number = len(products)
        imported_products_number = 0

        for p in products:
            category = Category.objects.get(pk=p.cat_id)
            product = Product(category=category, id=p.id, name=p.name, slug=p.slug.replace('_', '-'),
                              description=p.description,
                              detail=p.detail, price=p.price, discount=choice([0, 20, 30]))
            product.save()

            cursor.execute(
                "SELECT product_manager.id, product_manager.product_id, sizes.name AS size, "
                "product_manager.quantity FROM product_manager, sizes WHERE product_manager.product_id=%s AND "
                "product_manager.size_id=sizes.id", [product.id])

            product_items = namedtuple_fetchall(cursor)

            for p_item in product_items:
                ProductItem(product=product, size=p_item.size,
                            quantity=p_item.quantity).save()

            cursor.execute(
                "SELECT id, name, sort FROM image_manager WHERE product_id=%s", [product.id])

            product_images = namedtuple_fetchall(cursor)

            for p_image in product_images:
                with open(os.path.join(args.path_to_old_media, p_image.name), 'rb') as f:
                    product_image = ProductImage(
                        product=product, image_large=File(f), sort=p_image.sort)
                    product_image.save()

            imported_products_number += 1

            print(
                f'import products {(imported_products_number*100)//products_number}%', end='\r')
        print(
            f'imported products {imported_products_number}/{products_number}')


if __name__ == '__main__':
    main()
