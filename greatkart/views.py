from django.shortcuts import render
from store.models import Product, ReviewRating

from django.http import HttpResponse
from django.core.management import call_command

def run_migrate(request):
    call_command('migrate')
    return HttpResponse("Migrations completed.")

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }

    return render(request, 'home.html', context)
