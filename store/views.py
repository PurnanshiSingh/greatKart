from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category


# Create your views here.
def store(request, category_slug=None):
    categories=None
    products=None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()


    context = {
        'products': products,
        'product_count': product_count, 
    }
    print(f"prod",products)
    return render(request, 'store/store.html',context)

def product_detail(request, product_slug):
    print(f'product_slug: {product_slug}')
    try:
        product = Product.objects.get(slug=product_slug, is_available=True)
    except Product.DoesNotExist:
        product = Product(
        product_name="Default Product",
        slug="default-product",
        description="This is a default product because the requested product was not found.",
        price=0,
        images=None, 
        stock=0,
        is_available=False,
        category=None, 
    )

    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)
