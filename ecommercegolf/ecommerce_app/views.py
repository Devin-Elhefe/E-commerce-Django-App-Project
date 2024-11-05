from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Cart, CartItem, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.views.decorators import staff_member_required

from django import forms

from django.contrib.auth.decorators import login_required

from django.http import HttpResponse

def home(request):
    featured_products = Product.objects.filter(featured=True)
    return render(request, 'home.html', {'featured_products': featured_products})

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

@staff_member_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/update_product.html', {'form': form, 'product': product})

@staff_member_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'product/delete_product.html', {'product': product})






@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart = request.user.cart
    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    # quantity = int(request.POST.get('quantity', 1))
    
    # adding products or updating qty in cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not item_created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    
    return redirect('cart')

@login_required
def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart')
    
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

@login_required
def checkout(request):
    cart = request.user.cart
    cart_items = cart.items.all()
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, total_price=total_price)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price_at_purchase=item.product.price)
        cart.items.all().delete() # clear the cart after checkout
        return redirect('order_history') # redirect to order history page after checkout
    return render(request, 'cart/checkout.html', {'cart_items': cart_items, 'total_price': total_price})
    
    
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orderhistory.html', {'orders': orders})

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category']
        
@staff_member_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product/create_product.html', {'form': form})

