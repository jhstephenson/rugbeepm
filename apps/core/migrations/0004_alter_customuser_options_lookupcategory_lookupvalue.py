# Generated by Django 5.1.4 on 2024-12-23 23:36

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_add_user_fields'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'get_latest_by': 'date_joined', 'ordering': ['-date_joined'], 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.CreateModel(
            name='LookupCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier for this object', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when this object was created', verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='Date and time when this object was last updated', verbose_name='Updated Date')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this object is active. Inactive objects are treated as deleted.', verbose_name='Active')),
                ('notes', models.TextField(blank=True, help_text='Optional notes about this object', verbose_name='Notes')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Additional data stored as JSON', verbose_name='Metadata')),
                ('name', models.CharField(help_text='Name of the lookup category', max_length=100, unique=True, verbose_name='Name')),
                ('code', models.CharField(help_text='Unique code for the category (e.g., STATUS, PROJ_TYPE)', max_length=50, unique=True, verbose_name='Code')),
                ('description', models.TextField(blank=True, help_text='Description of what this category represents', verbose_name='Description')),
                ('is_system', models.BooleanField(default=False, help_text='Whether this is a system-defined category that cannot be modified', verbose_name='System Category')),
                ('created_by', models.ForeignKey(help_text='User who created this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('updated_by', models.ForeignKey(help_text='User who last updated this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Lookup Category',
                'verbose_name_plural': 'Lookup Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='LookupValue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, help_text='Unique identifier for this object', primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when this object was created', verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='Date and time when this object was last updated', verbose_name='Updated Date')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this object is active. Inactive objects are treated as deleted.', verbose_name='Active')),
                ('notes', models.TextField(blank=True, help_text='Optional notes about this object', verbose_name='Notes')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Additional data stored as JSON', verbose_name='Metadata')),
                ('name', models.CharField(help_text='Display name of the lookup value', max_length=100, verbose_name='Name')),
                ('code', models.CharField(help_text='Unique code within the category (e.g., ACTIVE, IN_PROGRESS)', max_length=50, verbose_name='Code')),
                ('description', models.TextField(blank=True, help_text='Description of what this value represents', verbose_name='Description')),
                ('sort_order', models.PositiveIntegerField(default=0, help_text='Order in which values should be displayed', verbose_name='Sort Order')),
                ('color', models.CharField(blank=True, help_text='Optional hex color code (e.g., #FF0000)', max_length=7, verbose_name='Color')),
                ('icon', models.CharField(blank=True, help_text='Optional icon identifier', max_length=50, verbose_name='Icon')),
                ('is_default', models.BooleanField(default=False, help_text='Whether this is the default value for its category', verbose_name='Default Value')),
                ('is_system', models.BooleanField(default=False, help_text='Whether this is a system-defined value that cannot be modified', verbose_name='System Value')),
                ('category', models.ForeignKey(help_text='The category this lookup value belongs to', on_delete=django.db.models.deletion.PROTECT, related_name='values', to='core.lookupcategory', verbose_name='Category')),
                ('created_by', models.ForeignKey(help_text='User who created this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('parent', models.ForeignKey(blank=True, help_text='Optional parent value for hierarchical lookups', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='core.lookupvalue', verbose_name='Parent Value')),
                ('updated_by', models.ForeignKey(help_text='User who last updated this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Lookup Value',
                'verbose_name_plural': 'Lookup Values',
                'ordering': ['category', 'sort_order', 'name'],
                'indexes': [models.Index(fields=['category', 'code'], name='core_lookup_categor_6727b5_idx'), models.Index(fields=['category', 'is_default'], name='core_lookup_categor_f4f61d_idx')],
                'unique_together': {('category', 'code')},
            },
        ),
    ]
