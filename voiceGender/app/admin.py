from django.contrib import admin
from . models import Contact, Product, Wishlist
# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id' , 'title' ,'category', 'price','product_imge']

admin.site.register(Wishlist)
admin.site.register(Contact)