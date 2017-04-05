from background_task import background
from django.apps import apps
from django.db import transaction
from common.util.parser import *
import tempfile

from django.core import files

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
			if prod["img_data"]:
				lf = tempfile.NamedTemporaryFile()
				lf.write(prod['img_data'])
				prd.image.save(prod['img_name'], files.File(lf))
			ctr, created = Category.objects.get_or_create(name=prod["category"])
			prd.category = ctr
			prd.save()

	# parse_products(shcedule=30)

parse_products()