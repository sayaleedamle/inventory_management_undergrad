from django.contrib import admin

from .forms import StockCreateForm

# Register your models here.
from .models import *



class StockCreateAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_category', 'product_name', 'product_quantity']
    form = StockCreateForm
    list_filter = ['product_category']
    search_fields = ['product_category', 'product_name']


admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)