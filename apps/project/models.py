from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import BaseModel, LookupValue
from decimal import Decimal
from django.utils import timezone

class Client(BaseModel):
    """
    Represents a client organization that projects are done for.
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_('Client Name'),
        help_text=_('Name of the client organization')
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Client Code'),
        help_text=_('Unique identifier for the client')
    )
    industry = models.ForeignKey(
        'core.LookupValue',
        on_delete=models.PROTECT,
        limit_choices_to={'category__code': 'INDUSTRY'},
        related_name='clients',
        verbose_name=_('Industry'),
        null=True,
        blank=True
    )
    primary_contact_name = models.CharField(
        max_length=200,
        verbose_name=_('Primary Contact Name'),
        blank=True
    )
    primary_contact_email = models.EmailField(
        verbose_name=_('Primary Contact Email'),
        blank=True
    )
    primary_contact_phone = models.CharField(
        max_length=50,
        verbose_name=_('Primary Contact Phone'),
        blank=True
    )
    billing_address = models.TextField(
        verbose_name=_('Billing Address'),
        blank=True
    )
    billing_email = models.EmailField(
        verbose_name=_('Billing Email'),
        blank=True
    )
    default_billing_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Default Billing Rate'),
        help_text=_('Default hourly billing rate for this client'),
        null=True,
        blank=True
    )
    payment_terms = models.CharField(
        max_length=100,
        verbose_name=_('Payment Terms'),
        blank=True,
        help_text=_('e.g., Net 30, Due on Receipt')
    )

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')
        ordering = ['name']

    def __str__(self):
        return self.name

class Project(BaseModel):
    """
    Represents a project in the system.
    """
    name = models.CharField(
        max_length=200,
        verbose_name=_('Project Name'),
        help_text=_('Name of the project')
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_('Project Code'),
        help_text=_('Unique code/identifier for the project')
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='projects',
        verbose_name=_('Client')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description'),
        help_text=_('Detailed description of the project')
    )
    status = models.ForeignKey(
        'core.LookupValue',
        on_delete=models.PROTECT,
        limit_choices_to={'category__code': 'PROJECT_STATUS'},
        related_name='projects',
        verbose_name=_('Status')
    )
    priority = models.ForeignKey(
        'core.LookupValue',
        on_delete=models.PROTECT,
        limit_choices_to={'category__code': 'PRIORITY'},
        related_name='priority_projects',
        verbose_name=_('Priority')
    )
    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Start Date'),
        help_text=_('When the project is scheduled to start')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('End Date'),
        help_text=_('When the project is scheduled to end')
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='managed_projects',
        verbose_name=_('Project Manager')
    )
    team_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ProjectMember',
        through_fields=('project', 'user'),
        related_name='project_memberships',
        verbose_name=_('Team Members')
    )
    budget_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Budget Amount'),
        help_text=_('Total budget for the project'),
        null=True,
        blank=True
    )
    billing_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Billing Rate'),
        help_text=_('Default hourly billing rate for this project (overrides client rate)'),
        null=True,
        blank=True
    )
    estimated_hours = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Estimated Hours'),
        help_text=_('Estimated total hours for the project'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.code} - {self.name}"

    @property
    def is_completed(self):
        """Check if the project is marked as completed based on status"""
        return self.status.code == 'COMPLETED'

    @property
    def get_effective_billing_rate(self):
        """Get the effective billing rate (project rate or client default)"""
        return self.billing_rate or (self.client.default_billing_rate if self.client else None)

class ProjectMember(BaseModel):
    """
    Represents a team member's association with a project, including their role.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='memberships',
        verbose_name=_('Project')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='project_roles',
        verbose_name=_('Team Member')
    )
    role = models.ForeignKey(
        'core.LookupValue',
        on_delete=models.PROTECT,
        limit_choices_to={'category__code': 'PROJECT_ROLE'},
        related_name='project_members',
        verbose_name=_('Role')
    )
    join_date = models.DateField(
        auto_now_add=True,
        verbose_name=_('Join Date')
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('End Date'),
        help_text=_('Date when the member left or will leave the project')
    )
    billing_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Billing Rate'),
        help_text=_('Custom billing rate for this member (overrides project rate)'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Project Member')
        verbose_name_plural = _('Project Members')
        unique_together = [('project', 'user')]
        ordering = ['project', 'user']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role.name} on {self.project.code}"

    @property
    def is_active_member(self):
        """Check if the member is currently active on the project"""
        return self.end_date is None or self.end_date > timezone.now().date()

    @property
    def get_effective_billing_rate(self):
        """Get the effective billing rate (member rate, project rate, or client default)"""
        return self.billing_rate or self.project.get_effective_billing_rate

class Task(BaseModel):
    """
    Represents a task within a project that can be assigned to team members.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name=_('Project')
    )
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subtasks',
        verbose_name=_('Parent Task')
    )
    title = models.CharField(
        max_length=200,
        verbose_name=_('Title')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    status = models.ForeignKey(
        'core.LookupValue',
        on_delete=models.PROTECT,
        limit_choices_to={'category__code': 'TASK_STATUS'},
        related_name='tasks',
        verbose_name=_('Status')
    )
    priority = models.ForeignKey(
        'core.LookupValue',
        on_delete=models.PROTECT,
        limit_choices_to={'category__code': 'PRIORITY'},
        related_name='priority_tasks',
        verbose_name=_('Priority')
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name=_('Assigned To')
    )
    due_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Due Date')
    )
    estimated_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Estimated Hours'),
        null=True,
        blank=True
    )
    actual_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Actual Hours'),
        default=Decimal('0.00')
    )
    billable = models.BooleanField(
        default=True,
        verbose_name=_('Billable'),
        help_text=_('Whether time spent on this task is billable')
    )
    billing_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Billing Rate'),
        help_text=_('Custom billing rate for this task (overrides project rate)'),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
        ordering = ['project', 'due_date', 'priority']

    def __str__(self):
        return f"{self.project.code} - {self.title}"

    @property
    def is_completed(self):
        """Check if the task is marked as completed based on status"""
        return self.status.code == 'COMPLETED'

    @property
    def get_effective_billing_rate(self):
        """Get the effective billing rate (task rate, assigned member rate, project rate, or client default)"""
        if self.billing_rate:
            return self.billing_rate
        if self.assigned_to:
            member = self.project.memberships.filter(user=self.assigned_to).first()
            if member and member.billing_rate:
                return member.billing_rate
        return self.project.get_effective_billing_rate

class TimeEntry(BaseModel):
    """
    Records time spent by team members on project tasks.
    """
    task = models.ForeignKey(
        Task,
        on_delete=models.PROTECT,
        related_name='time_entries',
        verbose_name=_('Task')
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='time_entries',
        verbose_name=_('User')
    )
    date = models.DateField(
        verbose_name=_('Date')
    )
    hours = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.00')),
            MaxValueValidator(Decimal('24.00'))
        ],
        verbose_name=_('Hours')
    )
    description = models.TextField(
        verbose_name=_('Description'),
        help_text=_('Description of work performed')
    )
    billable = models.BooleanField(
        default=True,
        verbose_name=_('Billable'),
        help_text=_('Whether this time entry is billable')
    )
    billing_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name=_('Billing Rate'),
        help_text=_('Rate at which this time was billed'),
        null=True,
        blank=True
    )
    billing_status = models.ForeignKey(
        'core.LookupValue',
        on_delete=models.PROTECT,
        limit_choices_to={'category__code': 'BILLING_STATUS'},
        related_name='time_entries',
        verbose_name=_('Billing Status')
    )

    class Meta:
        verbose_name = _('Time Entry')
        verbose_name_plural = _('Time Entries')
        ordering = ['-date', '-created_date']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.task.project.code} - {self.date}"

    def save(self, *args, **kwargs):
        # Update task actual hours
        if not self.pk:  # Only on creation
            self.task.actual_hours += self.hours
            self.task.save()
        super().save(*args, **kwargs)

    @property
    def get_effective_billing_rate(self):
        """Get the effective billing rate at time of entry"""
        return self.billing_rate or self.task.get_effective_billing_rate

    @property
    def billable_amount(self):
        """Calculate the billable amount for this time entry"""
        if not self.billable:
            return Decimal('0.00')
        rate = self.get_effective_billing_rate
        return rate * self.hours if rate else Decimal('0.00')
