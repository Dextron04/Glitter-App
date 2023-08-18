from django.urls import path
from . import views
from views import preTemplateView

urlpatterns = [
    path('', preTemplateView, name='pretemplate'),
]