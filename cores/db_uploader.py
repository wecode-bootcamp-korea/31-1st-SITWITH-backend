import os, django, csv, sys

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "practice.settings")
django.setup()

from products.models import *

CSV_PATH_CATEGORY = './cores/csv/01_category.csv'

with open(CSV_PATH_CATEGORY, encoding='utf-8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Category.objects.create(
                name = row[1]
            )
            
CSV_PATH_PRODUCT = './cores/csv/02_product.csv'

with open(CSV_PATH_PRODUCT, encoding='utf-8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Product.objects.create(
                name = row[1],
                price = row[2],
                category = Category.objects.get(name = row[3])
            )
            
CSV_PATH_COLOR = './cores/csv/03_color.csv'

with open(CSV_PATH_COLOR, encoding='utf-8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Color.objects.create(
                name = row[1]
            )

CSV_PATH_IMAGE = './cores/csv/04_image.csv'

with open(CSV_PATH_IMAGE, encoding='utf-8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            Image.objects.create(
                image_url = row[1],
                sequence = row[2],
                color = Color.objects.get(name = row[3]),
                product = Product.objects.get(name = row[4])
            )
            
CSV_PATH_PRODUCTCOLOR = './cores/csv/05_productcolor.csv'

with open(CSV_PATH_PRODUCTCOLOR, encoding='utf-8') as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        if row[0]:
            ProductColor.objects.create(
                color = Color.objects.get(name = row[1]),
                product = Product.objects.get(name = row[2])
            )