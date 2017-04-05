from django.shortcuts import render, get_object_or_404, render_to_response
from .models import Category, Product

# Страница с товарами
def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'webapp/hfiles/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

# Страница товара
def ProductDetail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    return render(request, 'webapp/hfiles/card.html',
                             {'product': product})


def ProductSearch(request):
    search_text = ''
    if request.method == "GET":
        search_text = request.GET['search']
    else:
        search_text = ''
    print(u"Search text: ", search_text)

    categories = Category.objects.all()  
    products = Product.objects.filter(name__contains=search_text)

    return render(request, 'webapp/hfiles/list.html', {
        'categories': categories,
        'products': products
    })