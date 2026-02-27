from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import User, EmailVerification


class EmailVerificationInline(admin.StackedInline):
    model = EmailVerification
    readonly_fields = ('token', 'created_at', 'is_expired')
    verbose_name_plural = "Email Verification"
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    ordering = ('-created_at',)

    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser',
        'is_active',
        'is_verified',
        'created_at',
    )

    list_filter = (
        'is_staff',
        'is_superuser',
        'is_active',
        'is_verified',
        'created_at',
    )

    search_fields = (
        'email',
        'username',
        'first_name',
        'last_name',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
        'last_login',
    )

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),

        ("Personal info", {
            "fields": ("first_name", "last_name")
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_verified",
                "groups",
                "user_permissions",
            )
        }),

        ("Timestamps", {
            "fields": (
                "last_login",
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "first_name",
                "last_name",
                "password1",
                "password2",
                "is_staff",
                "is_active",
                "is_verified",
            ),
        }),
    )
    inlines = [EmailVerificationInline]


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "created_at", "is_used")
    list_filter = ("is_used", "created_at")
    search_fields = ("user__email", "token")
    readonly_fields = ("token", "created_at")
    actions = ["mark_as_used"]

    def mark_as_used(self, request, queryset):
        queryset.update(is_used=True)
    mark_as_used.short_description = "Mark selected tokens as used"