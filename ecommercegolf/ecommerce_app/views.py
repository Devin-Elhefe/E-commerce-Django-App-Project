from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem, Order
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

def home(request):
    return render(request, 'productlist.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'productlist.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'productdetail.html', {'product': product})

@login_required
def cart(request):
    cart = request.user.cart
    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    
    # adding products or updating qty in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    
    return redirect('cart')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orderhistory.html', {'orders': orders})

