from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LookupCategory, LookupValue

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)


@admin.register(LookupCategory)
class LookupCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_system', 'is_active')
    search_fields = ('name', 'code', 'description')
    list_filter = ('is_system', 'is_active')
    readonly_fields = ('id', 'created_date', 'updated_date', 'created_by', 'updated_by')
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'description')
        }),
        ('System Settings', {
            'fields': ('is_system', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('id', 'created_date', 'updated_date', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LookupValue)
class LookupValueAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'code', 'sort_order', 'is_default', 'is_system', 'is_active')
    list_filter = ('category', 'is_default', 'is_system', 'is_active')
    search_fields = ('name', 'code', 'description', 'category__name')
    readonly_fields = ('id', 'created_date', 'updated_date', 'created_by', 'updated_by')
    list_select_related = ('category',)
    fieldsets = (
        (None, {
            'fields': ('category', 'name', 'code', 'description')
        }),
        ('Display Options', {
            'fields': ('sort_order', 'color', 'icon')
        }),
        ('Hierarchy', {
            'fields': ('parent',),
            'classes': ('collapse',)
        }),
        ('System Settings', {
            'fields': ('is_default', 'is_system', 'is_active'),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('id', 'created_date', 'updated_date', 'created_by', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            if request.resolver_match.kwargs.get('object_id'):
                obj = self.get_object(request, request.resolver_match.kwargs['object_id'])
                if obj:
                    kwargs["queryset"] = LookupValue.objects.filter(
                        category=obj.category
                    ).exclude(id=obj.id)
            else:
                kwargs["queryset"] = LookupValue.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
