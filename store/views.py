from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category

# Create your views here.
def store(request, category_slug=None):
    categories=None
    products=None
    # print("category_slug", category_slug)
    # print("product_slug", products)
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
    return render(request, 'store/store.html',context)

def product_detail(request, category_slug, product_slug):
    print("category_slug:", category_slug)
    print("product_slug:", product_slug)
    
    # Initialize product and category as None
    product = None
    category = None

    try:
        # Attempt to get the category and product based on slugs
        category = Category.objects.get(slug=category_slug)
        product = Product.objects.get(slug=product_slug, category=category, is_available=True)
    except Category.DoesNotExist:
        print(f"Category with slug '{category_slug}' not found.")
    except Product.DoesNotExist:
        print(f"Product with slug '{product_slug}' not found in category '{category_slug}'.")

    # If either category or product is None, use a default product
    if not category or not product:
        product = Product(
            product_name="Default Product",
            slug="default-product",
            description="This is a default product because the requested product or category was not found.",
            price=0,
            images=None,
            stock=0,
            is_available=False,
            category=None,
        )
        print("Displaying default product.")

    context = {
        'product': product,
    }
    return render(request, 'store/product_detail.html', context)

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)