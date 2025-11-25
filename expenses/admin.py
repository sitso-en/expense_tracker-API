from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'date', 'notes', 'category']
    autocomplete_fields = ['category']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_expenditure']
    search_fields = ['expense']