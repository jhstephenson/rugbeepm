from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, HTML
from . import models
from django.contrib.auth import get_user_model

class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = [
            'name', 'code', 'industry', 'primary_contact_name',
            'primary_contact_email', 'primary_contact_phone',
            'billing_address', 'billing_email', 'default_billing_rate',
            'payment_terms', 'notes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('code', css_class='col-md-3'),
                Column('industry', css_class='col-md-3'),
            ),
            Row(
                Column('primary_contact_name', css_class='col-md-4'),
                Column('primary_contact_email', css_class='col-md-4'),
                Column('primary_contact_phone', css_class='col-md-4'),
            ),
            Row(
                Column('billing_address', css_class='col-md-6'),
                Column(
                    Row(
                        Column('billing_email', css_class='col-12'),
                        Column('default_billing_rate', css_class='col-md-6'),
                        Column('payment_terms', css_class='col-md-6'),
                    ),
                    css_class='col-md-6'
                ),
            ),
            'notes',
            Submit('submit', _('Save Client'), css_class='btn-primary')
        )

class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        fields = [
            'name', 'code', 'client', 'description', 'status',
            'priority', 'start_date', 'end_date', 'manager',
            'budget_amount', 'billing_rate', 'estimated_hours',
            'notes'
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6'),
                Column('code', css_class='col-md-3'),
                Column('client', css_class='col-md-3'),
            ),
            Row(
                Column('status', css_class='col-md-4'),
                Column('priority', css_class='col-md-4'),
                Column('manager', css_class='col-md-4'),
            ),
            Row(
                Column('start_date', css_class='col-md-3'),
                Column('end_date', css_class='col-md-3'),
                Column('budget_amount', css_class='col-md-2'),
                Column('billing_rate', css_class='col-md-2'),
                Column('estimated_hours', css_class='col-md-2'),
            ),
            'description',
            'notes',
            Submit('submit', _('Save Project'), css_class='btn-primary')
        )

class ProjectMemberForm(forms.ModelForm):
    class Meta:
        model = models.ProjectMember
        fields = ['user', 'role', 'billing_rate']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        if project:
            self.instance.project = project
            # Exclude users who are already members
            existing_members = project.memberships.filter(end_date__isnull=True).values_list('user_id', flat=True)
            self.fields['user'].queryset = get_user_model().objects.exclude(id__in=existing_members)

class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = [
            'project', 'parent_task', 'title', 'description',
            'status', 'priority', 'assigned_to', 'due_date',
            'estimated_hours', 'billable', 'billing_rate', 'notes'
        ]
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        if project:
            self.fields['project'].initial = project
            self.fields['project'].widget = forms.HiddenInput()
            self.fields['parent_task'].queryset = models.Task.objects.filter(project=project)
        
        self.helper.layout = Layout(
            Row(
                Column('project', css_class='col-md-6'),
                Column('parent_task', css_class='col-md-6'),
            ) if not project else 'parent_task',
            Row(
                Column('title', css_class='col-md-12'),
            ),
            Row(
                Column('status', css_class='col-md-3'),
                Column('priority', css_class='col-md-3'),
                Column('assigned_to', css_class='col-md-3'),
                Column('due_date', css_class='col-md-3'),
            ),
            Row(
                Column('estimated_hours', css_class='col-md-4'),
                Column('billable', css_class='col-md-4'),
                Column('billing_rate', css_class='col-md-4'),
            ),
            'description',
            'notes',
            Submit('submit', _('Save Task'), css_class='btn-primary')
        )

class TimeEntryForm(forms.ModelForm):
    class Meta:
        model = models.TimeEntry
        fields = [
            'task', 'date', 'hours', 'description',
            'billable', 'billing_rate', 'billing_status'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, user=None, task=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        if user:
            self.instance.user = user
        if task:
            self.fields['task'].initial = task
            self.fields['task'].widget = forms.HiddenInput()
        else:
            # Only show tasks assigned to the user
            self.fields['task'].queryset = models.Task.objects.filter(
                assigned_to=user,
                status__category__code='TASK_STATUS',
                status__code__in=['TODO', 'IN_PROGRESS', 'REVIEW']
            )
        
        self.helper.layout = Layout(
            Row(
                Column('task', css_class='col-md-12') if not task else None,
                Column('date', css_class='col-md-4'),
                Column('hours', css_class='col-md-4'),
                Column('billable', css_class='col-md-4'),
            ),
            Row(
                Column('billing_rate', css_class='col-md-6'),
                Column('billing_status', css_class='col-md-6'),
            ),
            'description',
            Submit('submit', _('Save Time Entry'), css_class='btn-primary')
        )

    def clean_hours(self):
        hours = self.cleaned_data['hours']
        if hours <= 0:
            raise forms.ValidationError(_('Hours must be greater than 0'))
        if hours > 24:
            raise forms.ValidationError(_('Hours cannot exceed 24'))
        return hours
