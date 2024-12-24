from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count
from django.utils.html import format_html
from . import models

@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'industry', 'primary_contact_name', 'project_count', 'is_active')
    list_filter = ('industry', 'is_active')
    search_fields = ('name', 'code', 'primary_contact_name', 'primary_contact_email')
    readonly_fields = ('created_date', 'updated_date', 'created_by', 'updated_by')
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'industry', 'is_active')
        }),
        (_('Contact Information'), {
            'fields': ('primary_contact_name', 'primary_contact_email', 'primary_contact_phone')
        }),
        (_('Billing Information'), {
            'fields': ('billing_address', 'billing_email', 'default_billing_rate', 'payment_terms')
        }),
        (_('Notes & Metadata'), {
            'fields': ('notes', 'metadata'),
            'classes': ('collapse',)
        }),
        (_('Audit Information'), {
            'fields': ('created_date', 'created_by', 'updated_date', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def project_count(self, obj):
        count = obj.projects.count()
        return format_html('<a href="?client__id__exact={}">{}</a>', obj.id, count)
    project_count.short_description = _('Projects')

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class ProjectMemberInline(admin.TabularInline):
    model = models.ProjectMember
    extra = 0
    fields = ('user', 'role', 'join_date', 'end_date', 'billing_rate')
    readonly_fields = ('created_date', 'updated_date')

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'client', 'manager', 'status', 'priority', 
                   'start_date', 'end_date', 'budget_status', 'is_active')
    list_filter = ('status', 'priority', 'client', 'is_active')
    search_fields = ('name', 'code', 'description')
    readonly_fields = ('created_date', 'updated_date', 'created_by', 'updated_by')
    inlines = [ProjectMemberInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'client', 'description', 'is_active')
        }),
        (_('Status & Priority'), {
            'fields': ('status', 'priority')
        }),
        (_('Schedule'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Team'), {
            'fields': ('manager',)
        }),
        (_('Budget & Billing'), {
            'fields': ('budget_amount', 'billing_rate', 'estimated_hours')
        }),
        (_('Notes & Metadata'), {
            'fields': ('notes', 'metadata'),
            'classes': ('collapse',)
        }),
        (_('Audit Information'), {
            'fields': ('created_date', 'created_by', 'updated_date', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def budget_status(self, obj):
        if not obj.budget_amount:
            return '-'
        actual_amount = obj.tasks.aggregate(
            total=Sum('time_entries__hours', 
                     filter={'time_entries__billable': True})
        )['total'] or 0
        budget = float(obj.budget_amount)
        actual = float(actual_amount * (obj.billing_rate or 0))
        percentage = (actual / budget * 100) if budget else 0
        
        if percentage > 90:
            color = 'red'
        elif percentage > 75:
            color = 'orange'
        else:
            color = 'green'
        
        return format_html(
            '<span style="color: {}">${:,.2f} / ${:,.2f} ({:.1f}%)</span>',
            color, actual, budget, percentage
        )
    budget_status.short_description = _('Budget Status')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class SubtaskInline(admin.TabularInline):
    model = models.Task
    fk_name = 'parent_task'
    extra = 0
    fields = ('title', 'status', 'priority', 'assigned_to', 'due_date', 'estimated_hours')
    readonly_fields = ('actual_hours',)

@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'status', 'priority', 'assigned_to', 
                   'due_date', 'progress', 'is_active')
    list_filter = ('project', 'status', 'priority', 'assigned_to', 'is_active', 'billable')
    search_fields = ('title', 'description', 'project__name', 'project__code')
    readonly_fields = ('actual_hours', 'created_date', 'updated_date', 'created_by', 'updated_by')
    inlines = [SubtaskInline]
    fieldsets = (
        (None, {
            'fields': ('project', 'parent_task', 'title', 'description', 'is_active')
        }),
        (_('Status & Assignment'), {
            'fields': ('status', 'priority', 'assigned_to')
        }),
        (_('Schedule & Effort'), {
            'fields': ('due_date', 'estimated_hours', 'actual_hours')
        }),
        (_('Billing'), {
            'fields': ('billable', 'billing_rate')
        }),
        (_('Notes & Metadata'), {
            'fields': ('notes', 'metadata'),
            'classes': ('collapse',)
        }),
        (_('Audit Information'), {
            'fields': ('created_date', 'created_by', 'updated_date', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def progress(self, obj):
        if not obj.estimated_hours:
            return '-'
        percentage = (float(obj.actual_hours) / float(obj.estimated_hours) * 100)
        if percentage > 110:
            color = 'red'
        elif percentage > 90:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="color: {}">{:.1f}h / {:.1f}h ({:.1f}%)</span>',
            color, float(obj.actual_hours), float(obj.estimated_hours), percentage
        )
    progress.short_description = _('Progress')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(models.TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'task', 'project_code', 'hours', 
                   'billable_amount', 'billing_status', 'is_active')
    list_filter = ('date', 'user', 'task__project', 'billable', 'billing_status', 'is_active')
    search_fields = ('description', 'task__title', 'task__project__name', 'task__project__code')
    readonly_fields = ('created_date', 'updated_date', 'created_by', 'updated_by')
    fieldsets = (
        (None, {
            'fields': ('task', 'user', 'date', 'hours', 'description', 'is_active')
        }),
        (_('Billing'), {
            'fields': ('billable', 'billing_rate', 'billing_status')
        }),
        (_('Notes & Metadata'), {
            'fields': ('notes', 'metadata'),
            'classes': ('collapse',)
        }),
        (_('Audit Information'), {
            'fields': ('created_date', 'created_by', 'updated_date', 'updated_by'),
            'classes': ('collapse',)
        }),
    )

    def project_code(self, obj):
        return obj.task.project.code
    project_code.short_description = _('Project')
    project_code.admin_order_field = 'task__project__code'

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'task', 'task__project', 'user'
        )
