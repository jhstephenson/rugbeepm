from django.urls import path, include
from . import views

app_name = 'project'

urlpatterns = [
    path('api/', include('apps.project.api.urls')),
    # Add your URL patterns here
]