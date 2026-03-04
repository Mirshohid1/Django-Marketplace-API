from django.contrib import admin
from django.db.models import Count
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parent",
        "is_active",
        "children_count",
        "created_at",
    )

    list_filter = ("is_active", "created_at")
    search_fields = ("name", "slug")
    readonly_fields = ("created_at", "updated_at")

    prepopulated_fields = {"slug": ("name",)}

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(children_total=Count("children"))

    def children_count(self, obj):
        return obj.children_total

    children_count.short_description = "Children"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "owner",
        "category",
        "price",
        "status",
        "is_deleted",
        "created_at",
    )

    list_filter = (
        "status",
        "is_deleted",
        "category",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "slug",
        "owner__email",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = ("owner", "category")

    list_select_related = ("owner", "category")

    ordering = ("-created_at",)

    actions = (
        "approve_products",
        "archive_products",
        "soft_delete_products",
        "restore_products",
    )

    def get_queryset(self, request):
        return Product.all_objects.select_related("owner", "category")


    @admin.action(description="Approve selected products")
    def approve_products(self, request, queryset):
        for product in queryset:
            product.approve()

    @admin.action(description="Archive selected products")
    def archive_products(self, request, queryset):
        for product in queryset.filter(status=Product.Status.APPROVED):
            product.archive()

    @admin.action(description="Soft delete selected products")
    def soft_delete_products(self, request, queryset):
        for product in queryset:
            product.soft_delete()

    @admin.action(description="Restore selected products")
    def restore_products(self, request, queryset):
        for product in queryset:
            product.restore()
