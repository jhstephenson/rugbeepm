from django import forms
from .models import LookupCategory, LookupValue
from .models import UserProfile, CustomUser  # Import UserProfile model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _


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
        fields = ['name', 'code', 'description', 'sort_order', 'parent', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Username"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class UserProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'phone_number', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country', 'bio', 'birth_date'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'address_line1': _('Address Line 1'),
            'address_line2': _('Address Line 2'),
            'postal_code': _('Postal/ZIP Code'),
        }
        help_texts = {
            'avatar': _('Upload a profile picture (optional)'),
            'bio': _('Tell us a little about yourself'),
            'birth_date': _('Format: YYYY-MM-DD'),
        }


class UserProfileForm2(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'phone_number', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country', 'bio', 'birth_date'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            if field == 'avatar':
                self.fields[field].widget.attrs.update({
                    'class': 'form-control-file'
                })
