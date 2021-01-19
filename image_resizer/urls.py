"""image_resizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from resizer import views as resizer_views

urlpatterns = [
    # Можно вынести в resizer/urls.py, но нет смысла в мелком тестовом задании
    path('', resizer_views.ImageListView.as_view(), name='image_list'),
    path('detail/<int:pk>/', resizer_views.ImageDetailView.as_view(), name='image_detail'),

    path('new/', resizer_views.ImageCreateView.as_view(), name='image_create'),
    path('resize/<int:pk>/', resizer_views.ImageResizeView.as_view(), name='image_resize'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)