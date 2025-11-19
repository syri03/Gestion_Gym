# gym_project/urls.py
# gym_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', RedirectView.as_view(pattern_name='accounts:dashboard')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]