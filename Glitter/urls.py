from django.urls import path
from . import views
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