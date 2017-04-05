from background_task import background
from django.apps import apps
from django.db import transaction
from common.util.parser import *

@background(queue='parser')
def parse_products():
	products = do_it()

	with transaction.atomic():

		Product = apps.get_model('webapp', 'Product')
		Category = apps.get_model('webapp', 'Category')

		for prod in products:
			prd, created =Product.objects.get_or_create(pk=prod['product_id'])
			prd.name = prod["name"]
			prd.price = prod["price"]
			prd.description = prod["descriptions"]
			prd.slug = prod['product_id']
			prd.image = prod['image']
			ctr, created = Category.objects.get_or_create(name=prod["category"])
			prd.category = ctr
			prd.save()

	parse_products(shcedule=30)