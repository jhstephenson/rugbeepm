from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('get-started/', views.GetStartedView.as_view(), name='get-started'),
    path('about/', views.AboutView.as_view(), name='about'),
    
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='core/auth/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Profile URLs
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    
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
