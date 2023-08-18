from django.urls import path
from . import views
from Glitter.views import preTemplateView

urlpatterns = [
    path('', preTemplateView, name='pretemplate'),
]