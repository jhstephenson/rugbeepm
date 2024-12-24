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
    list_display = ('name', 'code', 'is_system', 'is_active', 'created_date')
    list_filter = ('is_system', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_date', 'updated_date')
    ordering = ('name',)


@admin.register(LookupValue)
class LookupValueAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'code', 'sort_order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'code', 'description')
    raw_id_fields = ('category', 'parent')
    readonly_fields = ('created_date', 'updated_date', 'created_by', 'updated_by')
    ordering = ('category', 'sort_order', 'name')

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
