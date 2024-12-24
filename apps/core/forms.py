from django import forms
from .models import LookupCategory, LookupValue


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.TextInput, forms.NumberInput, forms.EmailInput, forms.URLInput)):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control', 'rows': 3})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})


class CategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = LookupCategory
        fields = ['name', 'code', 'description', 'is_system']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ValueForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = LookupValue
        fields = ['name', 'code', 'description', 'sort_order', 'color', 'icon', 'is_default', 'is_system', 'parent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'color': forms.TextInput(attrs={'type': 'color'}),
        }
