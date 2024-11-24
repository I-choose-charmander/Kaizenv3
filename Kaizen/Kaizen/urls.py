"""
URL configuration for Kaizen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import TemplateView
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/',views.custom_logout, name='logout'),
    #path('meal/',views.macromeals, name='meal'),
    path('pdf/', views.pdf, name='pdf'),
    #path('upload-csv/', views.upload_csv, name='upload_csv'),
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('macro/', views.get_macro_values, name='macro'),
    path('profile', views.profile,name='profile'),
    path('macro_results/',views.macro_results,name='macro_results'),
    path('update_profile', views.update_profile,name='update_profile'),
    path('food', views.food_intake, name='food'),
    path('food_api', views.get_api_data, name='food_api'),
    path('delete_meal/<id>',views.delete_meal, name='delete_meal'),
    path('update_meal/<id>', views.update_meal, name='update_meal'),
    path('food_result', views.food_result, name='food_result'),
    path('daily_totals', views.daily_totals_view, name='daily_totals'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('meal_choice', views.meal_choice, name='meal_choice')
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
