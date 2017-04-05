import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
from django.utils.crypto import get_random_string

domain = 'http://verda-m.ru'
products = []

def get_links(urlpage):
	global page
	html = urlopen

def get_page(url):
	headers = {'User-agent': 'Mozila/5.0'}
	url = url
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')
	return soup

def parser_category(category_url, category_name):
	print("Категория {}".format(category_name))
	category_page = get_page('{0}{1}'.format(domain, category_url))
	product_cards = category_page.select('.list_products .product a')

	for link in product_cards:
		parse_product(link['href'], link['data-name'], link['data-id'], category_name)

def main():
	main_page = get_page('{0}/catalog/arki/'.format(domain))
	aww = main_page.select('#bx_1847241719_2343 ul li')

	for li in aww:
		link = li.select('a')[0]
		parser_category(link['href'], link.text)


def parse_product(product_url, product_name, product_id, category_name):
	pr_p = get_page('{0}{1}'.format(domain, product_url))
	price = pr_p.select('meta[itemprop="price"]')[0]['content']
	img_link = pr_p.select('img.js-sm-gal_main-img')[0]['src']
	img_name = "{}.jpg".format(get_random_string(10, 'abcdefghijklmnopqrstuvwxyz0123456789'))
	img_data = urlopen("{0}{1}".format(domain, img_link)).read()
	description_l = pr_p.select('div[itemprop="description"]')[0].contents
	description = ""
	for line in description_l:
		description = description + str(line)
	
	product_data = {
		"product_id": product_id,
		"category": category_name,
		"name": product_name,
		"price": price,
		"descriptions": description,
		"img_data": img_data,
		"img_name": img_name
	}
	products.append(product_data)

def do_it():
	main()
	return products

if __name__ == '__main__':
	do_it()
