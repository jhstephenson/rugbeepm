from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib import messages
from django.shortcuts import redirect
from .models import LookupCategory, LookupValue
from .forms import CategoryForm, ValueForm


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'RugbeePM'
        return context


class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class CategoryListView(LoginRequiredMixin, SuperUserRequiredMixin, ListView):
    model = LookupCategory
    template_name = 'core/category/list.html'
    context_object_name = 'categories'
    ordering = ['name']

    def get_queryset(self):
        return super().get_queryset().prefetch_related('values')


class CategoryCreateView(LoginRequiredMixin, SuperUserRequiredMixin, CreateView):
    model = LookupCategory
    template_name = 'core/category/form.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('core:category-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Category "{form.instance.name}" created successfully.')
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = LookupCategory
    template_name = 'core/category/form.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('core:category-list')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Category "{form.instance.name}" updated successfully.')
        return super().form_valid(form)


class CategoryDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = LookupCategory
    template_name = 'core/category/confirm_delete.html'

    def get_success_url(self):
        return reverse('core:category-list')

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(request, f'Category "{category.name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)


class CategoryDetailView(LoginRequiredMixin, SuperUserRequiredMixin, DetailView):
    model = LookupCategory
    template_name = 'core/category/detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = self.object.values.all().order_by('sort_order', 'name')
        return context


class ValueCreateView(LoginRequiredMixin, SuperUserRequiredMixin, CreateView):
    model = LookupValue
    template_name = 'core/value/form.html'
    form_class = ValueForm

    def get_success_url(self):
        return reverse('core:category-detail', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = LookupCategory.objects.get(pk=self.kwargs['category_pk'])
        return context

    def form_valid(self, form):
        form.instance.category_id = self.kwargs['category_pk']
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Value "{form.instance.name}" created successfully.')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        category_id = self.kwargs['category_pk']
        form.fields['parent'].queryset = LookupValue.objects.filter(category_id=category_id)
        return form


class ValueUpdateView(LoginRequiredMixin, SuperUserRequiredMixin, UpdateView):
    model = LookupValue
    template_name = 'core/value/form.html'
    form_class = ValueForm

    def get_success_url(self):
        return reverse('core:category-detail', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object.category
        return context

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Value "{form.instance.name}" updated successfully.')
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['parent'].queryset = LookupValue.objects.filter(
            category=self.object.category
        ).exclude(pk=self.object.pk)
        return form


class ValueDeleteView(LoginRequiredMixin, SuperUserRequiredMixin, DeleteView):
    model = LookupValue
    template_name = 'core/value/confirm_delete.html'

    def get_success_url(self):
        return reverse('core:category-detail', kwargs={'pk': self.object.category.pk})

    def delete(self, request, *args, **kwargs):
        value = self.get_object()
        messages.success(request, f'Value "{value.name}" deleted successfully.')
        return super().delete(request, *args, **kwargs)
