from django.contrib import admin
from .models import (
    Category, Vendor, Product, Customer,
    Purchase, PurchaseDetail, Sale, SaleDetail
)

admin.site.register(Category)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Purchase)
admin.site.register(PurchaseDetail)
admin.site.register(Sale)
admin.site.register(SaleDetail)
