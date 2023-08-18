"""
URL configuration for GlitterProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from Glitter.views import display_user_options, handle_invalid_url, display_about, display_home
from Glitter.views import preTemplateView

urlpatterns = [
    path('', preTemplateView, name='pretemplate'),
    path('home/', display_home, name='display_home'),
    path('about/', display_about, name='display_about'),
    path('filter/', display_user_options, name="display_user_options"),
    path('<str:invalid_url>/', handle_invalid_url, name='handle_invalid_url'),
    path('filter/<str:invalid_url>/', handle_invalid_url, name='handle_invalid_url'),
    path('about/<str:invalid_url>/', handle_invalid_url, name='handle_invalid_url')
]
