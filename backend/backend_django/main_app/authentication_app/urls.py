"""
URL configuration for main_app project.

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

from django.urls import path
from . import views
urlpatterns = [
    path("api/register", views.signup),
    path("api/login", views.login),
    path("api/create_recipe", views.create_recipe),
     path('api/get_recipe/',views.getRecipe),
     path('api/create_recipe_public/',views.create_recipe_public),
     path('api/getRecipe_public/',views.getRecipe_public),
]
