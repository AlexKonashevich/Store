from django.shortcuts import render


# Create your views here.

def index(request):
    context = {
        'title': 'Магазин',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title': 'Каталог',
    }
    return render(request, 'products/products.html', context)
