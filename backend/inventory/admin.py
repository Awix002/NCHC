from django.contrib import admin
from .models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'name', 'category',
                    'quantity', 'unit_price', 'unit', 'vendor', 'purchase_date', 'expiry_date')
    list_display_links = ('id', 'name', )
    search_fields = ('name', 'vendor' )
    list_per_page = 25


admin.site.register(Inventory, InventoryAdmin)

