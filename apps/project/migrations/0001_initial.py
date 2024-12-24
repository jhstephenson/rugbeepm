# Generated by Django 5.1.4 on 2024-12-24 19:24

import django.core.validators
import django.db.models.deletion
import uuid
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0006_remove_lookupvalue_core_lookup_categor_6727b5_idx_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when this object was created', verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='Date and time when this object was last updated', verbose_name='Updated Date')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this object is active. Inactive objects are treated as deleted.', verbose_name='Active')),
                ('notes', models.TextField(blank=True, help_text='Optional notes about this object', verbose_name='Notes')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Additional data stored as JSON', verbose_name='Metadata')),
                ('name', models.CharField(help_text='Name of the client organization', max_length=200, verbose_name='Client Name')),
                ('code', models.CharField(help_text='Unique identifier for the client', max_length=50, unique=True, verbose_name='Client Code')),
                ('primary_contact_name', models.CharField(blank=True, max_length=200, verbose_name='Primary Contact Name')),
                ('primary_contact_email', models.EmailField(blank=True, max_length=254, verbose_name='Primary Contact Email')),
                ('primary_contact_phone', models.CharField(blank=True, max_length=50, verbose_name='Primary Contact Phone')),
                ('billing_address', models.TextField(blank=True, verbose_name='Billing Address')),
                ('billing_email', models.EmailField(blank=True, max_length=254, verbose_name='Billing Email')),
                ('default_billing_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Default hourly billing rate for this client', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Default Billing Rate')),
                ('payment_terms', models.CharField(blank=True, help_text='e.g., Net 30, Due on Receipt', max_length=100, verbose_name='Payment Terms')),
                ('created_by', models.ForeignKey(help_text='User who created this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('industry', models.ForeignKey(blank=True, limit_choices_to={'category__code': 'INDUSTRY'}, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='clients', to='core.lookupvalue', verbose_name='Industry')),
                ('updated_by', models.ForeignKey(help_text='User who last updated this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when this object was created', verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='Date and time when this object was last updated', verbose_name='Updated Date')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this object is active. Inactive objects are treated as deleted.', verbose_name='Active')),
                ('notes', models.TextField(blank=True, help_text='Optional notes about this object', verbose_name='Notes')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Additional data stored as JSON', verbose_name='Metadata')),
                ('name', models.CharField(help_text='Name of the project', max_length=200, verbose_name='Project Name')),
                ('code', models.CharField(help_text='Unique code/identifier for the project', max_length=50, unique=True, verbose_name='Project Code')),
                ('description', models.TextField(blank=True, help_text='Detailed description of the project', verbose_name='Description')),
                ('start_date', models.DateField(blank=True, help_text='When the project is scheduled to start', null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, help_text='When the project is scheduled to end', null=True, verbose_name='End Date')),
                ('budget_amount', models.DecimalField(blank=True, decimal_places=2, help_text='Total budget for the project', max_digits=12, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Budget Amount')),
                ('billing_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Default hourly billing rate for this project (overrides client rate)', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Billing Rate')),
                ('estimated_hours', models.DecimalField(blank=True, decimal_places=2, help_text='Estimated total hours for the project', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Estimated Hours')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='project.client', verbose_name='Client')),
                ('created_by', models.ForeignKey(help_text='User who created this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='managed_projects', to=settings.AUTH_USER_MODEL, verbose_name='Project Manager')),
                ('priority', models.ForeignKey(limit_choices_to={'category__code': 'PRIORITY'}, on_delete=django.db.models.deletion.PROTECT, related_name='priority_projects', to='core.lookupvalue', verbose_name='Priority')),
                ('status', models.ForeignKey(limit_choices_to={'category__code': 'PROJECT_STATUS'}, on_delete=django.db.models.deletion.PROTECT, related_name='projects', to='core.lookupvalue', verbose_name='Status')),
                ('updated_by', models.ForeignKey(help_text='User who last updated this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='ProjectMember',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when this object was created', verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='Date and time when this object was last updated', verbose_name='Updated Date')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this object is active. Inactive objects are treated as deleted.', verbose_name='Active')),
                ('notes', models.TextField(blank=True, help_text='Optional notes about this object', verbose_name='Notes')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Additional data stored as JSON', verbose_name='Metadata')),
                ('join_date', models.DateField(auto_now_add=True, verbose_name='Join Date')),
                ('end_date', models.DateField(blank=True, help_text='Date when the member left or will leave the project', null=True, verbose_name='End Date')),
                ('billing_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Custom billing rate for this member (overrides project rate)', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Billing Rate')),
                ('created_by', models.ForeignKey(help_text='User who created this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='project.project', verbose_name='Project')),
                ('role', models.ForeignKey(limit_choices_to={'category__code': 'PROJECT_ROLE'}, on_delete=django.db.models.deletion.PROTECT, related_name='project_members', to='core.lookupvalue', verbose_name='Role')),
                ('updated_by', models.ForeignKey(help_text='User who last updated this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='project_roles', to=settings.AUTH_USER_MODEL, verbose_name='Team Member')),
            ],
            options={
                'verbose_name': 'Project Member',
                'verbose_name_plural': 'Project Members',
                'ordering': ['project', 'user'],
                'unique_together': {('project', 'user')},
            },
        ),
        migrations.AddField(
            model_name='project',
            name='team_members',
            field=models.ManyToManyField(related_name='project_memberships', through='project.ProjectMember', to=settings.AUTH_USER_MODEL, verbose_name='Team Members'),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when this object was created', verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='Date and time when this object was last updated', verbose_name='Updated Date')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this object is active. Inactive objects are treated as deleted.', verbose_name='Active')),
                ('notes', models.TextField(blank=True, help_text='Optional notes about this object', verbose_name='Notes')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Additional data stored as JSON', verbose_name='Metadata')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('due_date', models.DateField(blank=True, null=True, verbose_name='Due Date')),
                ('estimated_hours', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Estimated Hours')),
                ('actual_hours', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=8, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Actual Hours')),
                ('billable', models.BooleanField(default=True, help_text='Whether time spent on this task is billable', verbose_name='Billable')),
                ('billing_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Custom billing rate for this task (overrides project rate)', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Billing Rate')),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL, verbose_name='Assigned To')),
                ('created_by', models.ForeignKey(help_text='User who created this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('parent_task', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subtasks', to='project.task', verbose_name='Parent Task')),
                ('priority', models.ForeignKey(limit_choices_to={'category__code': 'PRIORITY'}, on_delete=django.db.models.deletion.PROTECT, related_name='priority_tasks', to='core.lookupvalue', verbose_name='Priority')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='project.project', verbose_name='Project')),
                ('status', models.ForeignKey(limit_choices_to={'category__code': 'TASK_STATUS'}, on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='core.lookupvalue', verbose_name='Status')),
                ('updated_by', models.ForeignKey(help_text='User who last updated this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'ordering': ['project', 'due_date', 'priority'],
            },
        ),
        migrations.CreateModel(
            name='TimeEntry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True, help_text='Date and time when this object was created', verbose_name='Created Date')),
                ('updated_date', models.DateTimeField(auto_now=True, help_text='Date and time when this object was last updated', verbose_name='Updated Date')),
                ('is_active', models.BooleanField(default=True, help_text='Whether this object is active. Inactive objects are treated as deleted.', verbose_name='Active')),
                ('notes', models.TextField(blank=True, help_text='Optional notes about this object', verbose_name='Notes')),
                ('metadata', models.JSONField(blank=True, default=dict, help_text='Additional data stored as JSON', verbose_name='Metadata')),
                ('date', models.DateField(verbose_name='Date')),
                ('hours', models.DecimalField(decimal_places=2, max_digits=6, validators=[django.core.validators.MinValueValidator(Decimal('0.00')), django.core.validators.MaxValueValidator(Decimal('24.00'))], verbose_name='Hours')),
                ('description', models.TextField(help_text='Description of work performed', verbose_name='Description')),
                ('billable', models.BooleanField(default=True, help_text='Whether this time entry is billable', verbose_name='Billable')),
                ('billing_rate', models.DecimalField(blank=True, decimal_places=2, help_text='Rate at which this time was billed', max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Billing Rate')),
                ('billing_status', models.ForeignKey(limit_choices_to={'category__code': 'BILLING_STATUS'}, on_delete=django.db.models.deletion.PROTECT, related_name='time_entries', to='core.lookupvalue', verbose_name='Billing Status')),
                ('created_by', models.ForeignKey(help_text='User who created this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_created', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='time_entries', to='project.task', verbose_name='Task')),
                ('updated_by', models.ForeignKey(help_text='User who last updated this object', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='%(class)s_updated', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='time_entries', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Time Entry',
                'verbose_name_plural': 'Time Entries',
                'ordering': ['-date', '-created_date'],
            },
        ),
    ]