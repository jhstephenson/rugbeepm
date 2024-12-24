import os
import re
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Creates a Django app with a full directory structure and common files'

    def add_arguments(self, parser):
        parser.add_argument('app_name', type=str, help='The name of the app to create')

    def validate_app_name(self, app_name):
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', app_name):
            raise CommandError('App name must start with a letter or underscore and contain only letters, numbers, and underscores.')
        return app_name

    def handle(self, *args, **options):
        try:
            app_name = self.validate_app_name(options['app_name'])
            apps_dir = Path('apps')
            app_dir = apps_dir / app_name

            # Create app directory and start app
            os.makedirs(app_dir, exist_ok=True)
            self.stdout.write(f"Creating Django app '{app_name}'...")
            call_command('startapp', app_name, str(app_dir))

            # Create directory structure
            directories = [
                app_dir / 'templates' / app_name,
                app_dir / 'templates' / app_name / 'components',
                app_dir / 'templates' / app_name / 'emails',
                app_dir / 'templates' / app_name / 'forms',
                app_dir / 'templates' / app_name / 'layouts',
                app_dir / 'static' / app_name / 'css',
                app_dir / 'static' / app_name / 'js',
                app_dir / 'static' / app_name / 'images',
                app_dir / 'static' / app_name / 'fonts',
                app_dir / 'static' / app_name / 'scss',
                app_dir / 'api',
                app_dir / 'tests',
            ]

            for directory in directories:
                os.makedirs(directory, exist_ok=True)

            # Define file templates
            files = [
                ('forms.py', """from django import forms

# Create your forms here
"""),
                ('urls.py', f"""from django.urls import path, include
from . import views

app_name = '{app_name}'

urlpatterns = [
    path('api/', include('{app_name}.api.urls')),
    # Add your URL patterns here
]"""),
                ('filters.py', """import django_filters

# Create your filters here
"""),
                ('managers.py', """from django.db import models

# Create your model managers here
"""),
                ('utils.py', """from django.http import JsonResponse

def api_response(data=None, message=None, status=200, errors=None):
    response = {
        'status': 'success' if status < 400 else 'error',
        'message': message,
        'data': data,
        'errors': errors
    }
    return JsonResponse(response, status=status)"""),
                ('constants.py', """# Define your app constants here
"""),
                ('services.py', '''"""
Business logic and service layer functionality.
Keep your views thin by moving complex logic here.
"""

# Create your services here
'''),
                ('selectors.py', '''"""
Complex database queries and data retrieval logic.
Similar to services.py but focused on data selection.
"""

# Create your selectors here
'''),
                ('exceptions.py', '''"""Custom exceptions for this app."""

class CustomAppException(Exception):
    """Base exception for the app."""
    pass
'''),
                ('models.py', '''from django.db import models

class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created' and 'modified' fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# Create your models here
'''),
                ('views.py', '''from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# Create your views here
'''),
                ('admin.py', '''from django.contrib import admin

# Register your models here
'''),
                ('apps.py', f'''from django.apps import AppConfig


class {app_name.capitalize()}Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'

    def ready(self):
        """
        Import signal handlers and perform other initialization.
        """
        try:
            import apps.{app_name}.signals  # noqa
        except ImportError:
            pass
'''),
                ('api/__init__.py', ''),
                ('api/serializers.py', """from rest_framework import serializers

# Create your serializers here
"""),
                ('api/views.py', """from rest_framework import viewsets, permissions

# Create your API views here
"""),
                ('api/urls.py', """from django.urls import path

app_name = 'api'

urlpatterns = [
    # Add your API URL patterns here
]"""),
                ('tests/__init__.py', ''),
                ('tests/test_models.py', """from django.test import TestCase

# Create your model tests here
"""),
                ('tests/test_views.py', """from django.test import TestCase, Client
from django.urls import reverse

# Create your view tests here
"""),
                ('tests/test_forms.py', """from django.test import TestCase

# Create your form tests here
"""),
                ('tests/test_urls.py', """from django.test import TestCase
from django.urls import reverse, resolve

# Create your URL tests here
"""),
                ('tests/test_api.py', """from django.test import TestCase
from rest_framework.test import APIClient

# Create your API tests here
"""),
                ('tests/test_utils.py', """from django.test import TestCase

# Create your utility tests here
"""),
                ('tests/factories.py', '''"""Model factories for testing."""

from factory.django import DjangoModelFactory
from factory import Faker

# Create your factories here
# Example:
# class YourModelFactory(DjangoModelFactory):
#     name = Faker('name')
#
#     class Meta:
#         model = YourModel
'''),
                (f'templates/{app_name}/base.html', """{% extends "base.html" %}

{% block content %}
{% endblock %}"""),
                (f'templates/{app_name}/components/README.md', 'Store reusable template components here'),
                (f'templates/{app_name}/emails/README.md', 'Store email templates here'),
                (f'templates/{app_name}/forms/README.md', 'Store form templates here'),
                (f'templates/{app_name}/layouts/README.md', 'Store layout templates here'),
                (f'static/{app_name}/css/styles.css', '/* Main stylesheet */'),
                (f'static/{app_name}/js/main.js', '// Main JavaScript file'),
                (f'static/{app_name}/scss/main.scss', '// Main SCSS file'),
            ]

            # Create files
            for filename, content in files:
                filepath = app_dir / filename
                filepath.parent.mkdir(exist_ok=True)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)

            # Remove default tests.py
            tests_file = app_dir / 'tests.py'
            if tests_file.exists():
                tests_file.unlink()

            self.stdout.write(self.style.SUCCESS(f"""
Successfully created app '{app_name}' with full structure.
Next steps:
1. Add '{app_name}' to INSTALLED_APPS in settings.py as 'apps.{app_name}'
2. Include app URLs in project urls.py:
   path('{app_name}/', include('apps.{app_name}.urls')),
3. Run migrations if you've added models
4. Start building your views and templates"""))

        except Exception as e:
            raise CommandError(f"Failed to create app: {str(e)}")
