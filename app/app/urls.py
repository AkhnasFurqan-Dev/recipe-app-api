"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='frontend'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('recipes/', TemplateView.as_view(template_name='recipes.html'), name='recipes'),
    path('recipes/new/', TemplateView.as_view(template_name='recipe_form.html'), name='recipe-new'),
    path('recipes/edit/', TemplateView.as_view(template_name='recipe_form.html'), name='recipe-edit'),
    path('library/', TemplateView.as_view(template_name='library.html'), name='library'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='api-scheme'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-scheme'),
        name='api-docs',
    ),
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )
