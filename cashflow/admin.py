from django.contrib import admin

from .models import CashflowRecord, Category, Status, Subcategory, Type


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
    inlines = [CategoryInline]


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "type"]
    list_filter = ["type"]
    search_fields = ["name"]
    inlines = [SubcategoryInline]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "category"]
    list_filter = ["category"]
    search_fields = ["name"]


@admin.register(CashflowRecord)
class CashflowRecordAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "status",
        "type",
        "category",
        "subcategory",
        "amount",
    ]
    list_filter = ["status", "type", "category", "subcategory"]
    search_fields = ["comment"]
