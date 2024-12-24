from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base model that provides common fields for all models.
    
    Fields:
        id (UUIDField): Primary key using UUID4
        created_date (DateTimeField): Auto-set when object is created
        updated_date (DateTimeField): Auto-set when object is updated
        created_by (ForeignKey): User who created the object
        updated_by (ForeignKey): User who last updated the object
        is_active (BooleanField): Soft deletion status
        notes (TextField): Optional notes about the object
        metadata (JSONField): Flexible field for additional data
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('ID'),
        help_text=_('Unique identifier for this object')
    )
    
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created Date'),
        help_text=_('Date and time when this object was created')
    )
    
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated Date'),
        help_text=_('Date and time when this object was last updated')
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_created',
        verbose_name=_('Created By'),
        help_text=_('User who created this object'),
        null=True
    )
    
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='%(class)s_updated',
        verbose_name=_('Updated By'),
        help_text=_('User who last updated this object'),
        null=True
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active'),
        help_text=_('Whether this object is active. Inactive objects are treated as deleted.')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes'),
        help_text=_('Optional notes about this object')
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Metadata'),
        help_text=_('Additional data stored as JSON')
    )

    class Meta:
        abstract = True
        ordering = ['-created_date']
        get_latest_by = 'created_date'

    def __str__(self):
        """Default string representation using the ID."""
        return str(self.id)

    def save(self, *args, **kwargs):
        """
        Override save method to perform common operations:
        - Ensure metadata is a dict
        - Clean fields before saving
        """
        if self.metadata is None:
            self.metadata = {}
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """
        Soft delete the object by setting is_active to False.
        Use force_delete() for actual deletion.
        """
        self.is_active = False
        self.save(using=using)

    def force_delete(self, using=None, keep_parents=False):
        """Actually delete the object from the database."""
        super().delete(using=using, keep_parents=keep_parents)

    def restore(self):
        """Restore a soft-deleted object."""
        self.is_active = True
        self.save()


class CustomUser(AbstractUser):
    """
    Custom user model for the application.
    Add custom fields here as needed.
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        verbose_name=_('UUID'),
        help_text=_('Unique identifier for this user')
    )
    
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Created Date'),
        help_text=_('Date and time when this user was created')
    )
    
    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated Date'),
        help_text=_('Date and time when this user was last updated')
    )
    
    notes = models.TextField(
        blank=True,
        verbose_name=_('Notes'),
        help_text=_('Optional notes about this user')
    )
    
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Metadata'),
        help_text=_('Additional data stored as JSON')
    )

    class Meta(AbstractUser.Meta):
        ordering = ['-date_joined']
        get_latest_by = 'date_joined'

    def save(self, *args, **kwargs):
        """Ensure metadata is a dict and fields are clean before saving."""
        if self.metadata is None:
            self.metadata = {}
        self.full_clean()
        super().save(*args, **kwargs)


class LookupCategory(BaseModel):
    """
    Categories for lookup values (e.g., 'Status', 'ProjectType', 'ActivityType').
    This helps organize and group lookup values.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Name'),
        help_text=_('Name of the lookup category')
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Code'),
        help_text=_('Unique code for the category (e.g., STATUS, PROJ_TYPE)')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Description of what this category represents')
    )
    is_system = models.BooleanField(
        default=False,
        verbose_name=_('System Category'),
        help_text=_('Whether this is a system-defined category that cannot be modified')
    )

    class Meta:
        verbose_name = _('Lookup Category')
        verbose_name_plural = _('Lookup Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        super().save(*args, **kwargs)


class LookupValue(BaseModel):
    """
    Generic lookup values that can be used across the system.
    Each value belongs to a category and can have additional metadata.
    """
    category = models.ForeignKey(
        LookupCategory,
        on_delete=models.PROTECT,
        related_name='values',
        verbose_name=_('Category'),
        help_text=_('The category this lookup value belongs to')
    )
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name'),
        help_text=_('Display name of the lookup value')
    )
    code = models.CharField(
        max_length=50,
        verbose_name=_('Code'),
        help_text=_('Unique code within the category (e.g., ACTIVE, IN_PROGRESS)')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Description of what this value represents')
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Sort Order'),
        help_text=_('Order in which values should be displayed')
    )
    color = models.CharField(
        max_length=7,
        blank=True,
        verbose_name=_('Color'),
        help_text=_('Optional hex color code (e.g., #FF0000)')
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_('Icon'),
        help_text=_('Optional icon identifier')
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('Default Value'),
        help_text=_('Whether this is the default value for its category')
    )
    is_system = models.BooleanField(
        default=False,
        verbose_name=_('System Value'),
        help_text=_('Whether this is a system-defined value that cannot be modified')
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name=_('Parent Value'),
        help_text=_('Optional parent value for hierarchical lookups')
    )

    class Meta:
        verbose_name = _('Lookup Value')
        verbose_name_plural = _('Lookup Values')
        ordering = ['category', 'sort_order', 'name']
        unique_together = [('category', 'code')]
        indexes = [
            models.Index(fields=['category', 'code']),
            models.Index(fields=['category', 'is_default']),
        ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        self.code = self.code.upper()
        if self.is_default:
            # Ensure only one default value per category
            LookupValue.objects.filter(
                category=self.category,
                is_default=True
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class LookupManager:
    """
    Helper class to manage and access lookup values throughout the system.
    Usage:
        # In models.py:
        status = models.ForeignKey(
            'core.LookupValue',
            limit_choices_to={'category__code': 'STATUS'},
            on_delete=models.PROTECT
        )

        # In views/business logic:
        from apps.core.models import LookupManager
        
        lookup = LookupManager()
        active_status = lookup.get_value('STATUS', 'ACTIVE')
        all_statuses = lookup.get_values('STATUS')
        default_status = lookup.get_default('STATUS')
    """
    
    @staticmethod
    def get_category(category_code):
        """Get a lookup category by its code."""
        return LookupCategory.objects.filter(code=category_code).first()
    
    @staticmethod
    def get_value(category_code, value_code):
        """Get a specific lookup value by category and value codes."""
        return LookupValue.objects.filter(
            category__code=category_code,
            code=value_code
        ).first()
    
    @staticmethod
    def get_values(category_code, active_only=True):
        """Get all lookup values for a category."""
        queryset = LookupValue.objects.filter(category__code=category_code)
        if active_only:
            queryset = queryset.filter(is_active=True)
        return queryset.order_by('sort_order', 'name')
    
    @staticmethod
    def get_default(category_code):
        """Get the default value for a category."""
        return LookupValue.objects.filter(
            category__code=category_code,
            is_default=True
        ).first()
    
    @staticmethod
    def get_choices(category_code, include_blank=True):
        """Get choices suitable for form fields."""
        choices = [(v.id, v.name) for v in LookupManager.get_values(category_code)]
        if include_blank:
            choices.insert(0, ('', '---------'))
        return choices