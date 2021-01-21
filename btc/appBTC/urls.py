from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.index, name="index"),
  path('api/<tool>', views.api, name="api"),
  path('deslogar', views.deslogar, name="deslogar"),
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
