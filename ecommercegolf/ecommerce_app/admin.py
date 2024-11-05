from django.contrib import admin
from .models import Product, Category, Cart, CartItem, Order, OrderItem
# Register your models here.

admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)

# this will add an image upload field to the product admin page, allowing us to add or change images for each product.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'image', 'featured')
    fields = ('name', 'description', 'price', 'stock', 'category', 'image', 'featured')
    

admin.site.register(Product, ProductAdmin)