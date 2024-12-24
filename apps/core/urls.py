from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<uuid:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<uuid:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<uuid:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),
    
    # Value URLs
    path('categories/<uuid:category_pk>/values/new/', views.ValueCreateView.as_view(), name='value-create'),
    path('values/<uuid:pk>/edit/', views.ValueUpdateView.as_view(), name='value-update'),
    path('values/<uuid:pk>/delete/', views.ValueDeleteView.as_view(), name='value-delete'),
]
