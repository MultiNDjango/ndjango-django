from django.contrib import admin
from refrigerators.models import Grocery

@admin.register(Grocery)

class GroceryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'qty', 'in_date', 'exp_date', 'image']
    list_display_links = ['id', 'name']
    list_per_page = 10
    