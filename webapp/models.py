from django.db import models
from django.utils.safestring import mark_safe
from datetime import *
import os
from web import settings
from django.core.urlresolvers import reverse

class Category(models.Model):
	name = models.CharField(max_length=50, null=True, db_index=True, verbose_name="Категория")
	slug = models.SlugField(max_length=200, null=True, db_index=True, unique=True)
	class Meta:
		ordering = ['name']
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('webapp:ProductListByCategory', args=[self.slug])


class Product(models.Model):
	category = models.ForeignKey(Category, related_name='Product', null=True, verbose_name="Категория")
	name = models.CharField(max_length=50, null=True, db_index=True, verbose_name="Товар")
	slug = models.SlugField(max_length=200, null=True, db_index=True, verbose_name="Ссылка")
	price = models.DecimalField(max_digits=20, null=True, decimal_places=2, verbose_name="Цена")
	description = models.TextField(blank=True, null=True, verbose_name="Описание")
	image=models.ImageField(upload_to='images',null=True, blank=True)

	class Meta:
		ordering = ['name']
		index_together = [
			['id', 'slug']
		]
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'
    
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('webapp:ProductDetail', args=[self.id, self.slug])


