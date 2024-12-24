from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from django.db.models import Q, Sum, Count
from django.utils import timezone
from django.contrib.messages.views import SuccessMessageMixin
from . import models, forms
from apps.core.models import LookupCategory, LookupValue

class ClientListView(LoginRequiredMixin, ListView):
    model = models.Client
    template_name = 'project/client_list.html'
    context_object_name = 'clients'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(primary_contact_name__icontains=search)
            )
        return queryset.filter(is_active=True)

class ClientDetailView(LoginRequiredMixin, DetailView):
    model = models.Client
    template_name = 'project/client_detail.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_projects'] = self.object.projects.filter(
            is_active=True,
            status__code__in=['DRAFT', 'ACTIVE', 'ON_HOLD']
        )
        return context

class ClientCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Client
    form_class = forms.ClientForm
    template_name = 'project/client_form.html'
    success_url = reverse_lazy('project:client_list')
    success_message = _('Client "%(name)s" was created successfully')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ClientUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Client
    form_class = forms.ClientForm
    template_name = 'project/client_form.html'
    success_message = _('Client "%(name)s" was updated successfully')

    def get_success_url(self):
        return reverse_lazy('project:client_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ProjectListView(LoginRequiredMixin, ListView):
    model = models.Project
    template_name = 'project/project_list.html'
    context_object_name = 'projects'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        client = self.request.GET.get('client', '')

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search) |
                Q(client__name__icontains=search)
            )
        if status:
            queryset = queryset.filter(status__code=status)
        if client:
            queryset = queryset.filter(client_id=client)

        return queryset.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = LookupCategory.objects.filter(
            code='PROJECT_STATUS'
        )
        context['clients'] = models.Client.objects.filter(is_active=True)
        return context

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = models.Project
    template_name = 'project/project_detail.html'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['team_members'] = self.object.memberships.filter(
            end_date__isnull=True
        ).select_related('user', 'role')
        context['tasks'] = self.object.tasks.filter(
            parent_task__isnull=True
        ).select_related('status', 'priority', 'assigned_to')
        context['recent_time_entries'] = models.TimeEntry.objects.filter(
            task__project=self.object
        ).select_related('user', 'task').order_by('-date')[:5]
        return context

class ProjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'project/project_form.html'
    success_url = reverse_lazy('project:project_list')
    success_message = _('Project "%(name)s" was created successfully')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Project
    form_class = forms.ProjectForm
    template_name = 'project/project_form.html'
    success_message = _('Project "%(name)s" was updated successfully')

    def get_success_url(self):
        return reverse_lazy('project:project_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Project
    template_name = 'project/project_confirm_delete.html'
    success_url = reverse_lazy('project:projects')
    success_message = _('Project deleted successfully')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class ProjectMemberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.ProjectMember
    form_class = forms.ProjectMemberForm
    template_name = 'project/projectmember_form.html'
    success_message = _('Team member was added successfully')

    def get_project(self):
        return get_object_or_404(models.Project, pk=self.kwargs['project_id'])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project'] = self.get_project()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = self.get_project()
        return context

    def get_success_url(self):
        return reverse_lazy('project:project_detail', kwargs={'pk': self.kwargs['project_id']})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class TaskListView(LoginRequiredMixin, ListView):
    model = models.Task
    template_name = 'project/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        status = self.request.GET.get('status', '')
        project = self.request.GET.get('project', '')
        assigned = self.request.GET.get('assigned', '')

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(project__name__icontains=search)
            )
        if status:
            queryset = queryset.filter(status__code=status)
        if project:
            queryset = queryset.filter(project_id=project)
        if assigned == 'me':
            queryset = queryset.filter(assigned_to=self.request.user)
        elif assigned:
            queryset = queryset.filter(assigned_to_id=assigned)

        return queryset.filter(is_active=True).select_related(
            'project', 'status', 'priority', 'assigned_to'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = LookupCategory.objects.filter(
            code='TASK_STATUS'
        )
        context['projects'] = models.Project.objects.filter(is_active=True)
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    template_name = 'project/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtasks'] = self.object.subtasks.filter(
            is_active=True
        ).select_related('status', 'priority', 'assigned_to')
        context['time_entries'] = self.object.time_entries.select_related(
            'user', 'billing_status'
        ).order_by('-date')
        context['time_entry_form'] = forms.TimeEntryForm(
            user=self.request.user,
            task=self.object
        )
        return context

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'project/task_form.html'
    success_message = _('Task "%(title)s" was created successfully')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        project_id = self.kwargs.get('project_id')
        if project_id:
            kwargs['project'] = get_object_or_404(models.Project, pk=project_id)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('project:project_detail', kwargs={'pk': self.object.project.pk})

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = models.Task
    form_class = forms.TaskForm
    template_name = 'project/task_form.html'
    success_message = _('Task "%(title)s" was updated successfully')

    def get_success_url(self):
        return reverse_lazy('project:task_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Task
    template_name = 'project/task_confirm_delete.html'
    success_url = reverse_lazy('project:tasks')
    success_message = _('Task deleted successfully')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class TimeEntryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = models.TimeEntry
    form_class = forms.TimeEntryForm
    template_name = 'project/timeentry_form.html'
    success_message = _('Time entry was created successfully')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        task_id = self.kwargs.get('task_id')
        if task_id:
            kwargs['task'] = get_object_or_404(models.Task, pk=task_id)
        return kwargs

    def get_success_url(self):
        return reverse_lazy('project:task_detail', kwargs={'pk': self.object.task.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class TimeEntryUpdateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = models.TimeEntry
    form_class = forms.TimeEntryForm
    template_name = 'project/timeentry_form.html'
    success_message = _('Time entry was updated successfully')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('project:task_detail', kwargs={'pk': self.object.task.pk})

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)

class TimeEntryDeleteView(LoginRequiredMixin, DeleteView):
    model = models.TimeEntry
    template_name = 'project/timeentry_confirm_delete.html'
    success_message = _('Time entry deleted successfully')

    def get_success_url(self):
        return reverse_lazy('project:task_detail', kwargs={'pk': self.object.task.pk})

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class ProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'project/profile.html'
    success_url = reverse_lazy('project:profile')
    success_message = _('Profile updated successfully')

    def get_object(self, queryset=None):
        # Get or create the profile for the current user
        profile, created = models.UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_form_class(self):
        # Create a form class that includes both user and profile fields
        from django import forms
        
        class ProfileForm(forms.ModelForm):
            first_name = forms.CharField(max_length=150, required=False)
            last_name = forms.CharField(max_length=150, required=False)
            email = forms.EmailField()

            class Meta:
                model = models.UserProfile
                fields = [
                    'first_name', 'last_name', 'email',
                    'phone_number', 'address_line1', 'address_line2',
                    'city', 'state', 'postal_code', 'country',
                    'bio', 'birth_date', 'avatar'
                ]
                widgets = {
                    'birth_date': forms.DateInput(attrs={'type': 'date'}),
                }

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                if self.instance and self.instance.user:
                    self.fields['first_name'].initial = self.instance.user.first_name
                    self.fields['last_name'].initial = self.instance.user.last_name
                    self.fields['email'].initial = self.instance.user.email

            def save(self, commit=True):
                profile = super().save(commit=False)
                if commit:
                    # Save user fields
                    user = profile.user
                    user.first_name = self.cleaned_data['first_name']
                    user.last_name = self.cleaned_data['last_name']
                    user.email = self.cleaned_data['email']
                    user.save()
                    # Save profile
                    profile.save()
                return profile

        return ProfileForm

class CategoryListView(LoginRequiredMixin, ListView):
    model = LookupCategory
    template_name = 'project/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return LookupCategory.objects.filter(is_system=False)

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = LookupCategory
    template_name = 'project/category_form.html'
    fields = ['name', 'code', 'description']
    success_url = reverse_lazy('project:categories')

    def form_valid(self, form):
        form.instance.is_system = False
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = LookupCategory
    template_name = 'project/category_form.html'
    fields = ['name', 'code', 'description']
    success_url = reverse_lazy('project:categories')

    def get_queryset(self):
        return LookupCategory.objects.filter(is_system=False)

class CategoryDetailView(LoginRequiredMixin, DetailView):
    model = LookupCategory
    template_name = 'project/category_detail.html'
    context_object_name = 'category'

    def get_queryset(self):
        return LookupCategory.objects.filter(is_system=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = self.object.values.all()
        return context

class CategoryValueCreateView(LoginRequiredMixin, CreateView):
    model = LookupValue
    fields = ['code', 'label', 'description', 'order']
    template_name = 'project/category_value_form.html'

    def get_category(self):
        return get_object_or_404(LookupCategory, pk=self.kwargs['category_id'], is_system=False)

    def form_valid(self, form):
        form.instance.category = self.get_category()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project:category_detail', kwargs={'pk': self.kwargs['category_id']})

class CategoryValueUpdateView(LoginRequiredMixin, UpdateView):
    model = LookupValue
    fields = ['code', 'label', 'description', 'order']
    template_name = 'project/category_value_form.html'
    pk_url_kwarg = 'value_id'

    def get_category(self):
        return get_object_or_404(LookupCategory, pk=self.kwargs['category_id'], is_system=False)

    def get_queryset(self):
        return LookupValue.objects.filter(category=self.get_category())

    def get_success_url(self):
        return reverse_lazy('project:category_detail', kwargs={'pk': self.kwargs['category_id']})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('core:home')

    context = {
        'active_projects': models.Project.objects.filter(
            is_active=True,
            status__code__in=['DRAFT', 'ACTIVE', 'ON_HOLD']
        ).count(),
        'my_tasks': models.Task.objects.filter(
            is_active=True,
            assigned_to=request.user,
            status__code__in=['TODO', 'IN_PROGRESS', 'REVIEW']
        ).count(),
        'recent_time_entries': models.TimeEntry.objects.filter(
            user=request.user
        ).select_related('task', 'task__project').order_by('-date')[:5],
        'unbilled_hours': models.TimeEntry.objects.filter(
            user=request.user,
            billable=True,
            billing_status__code='UNBILLED'
        ).aggregate(total=Sum('hours'))['total'] or 0,
    }
    
    return render(request, 'project/dashboard.html', context)
