"""
URL configuration for pokedex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from home import views as home_views
from pokemon_detail import views as pokemon_detail_views
from pokemon_query import views as pokemon_query_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_views.home, name='home'),
    path('pokemon/<int:pokemon_id>/', pokemon_detail_views.pokemon_detail, name='pokemon_detail'),
    path('pokemon/<int:pokemon_id>/query/', pokemon_query_views.pokemon_query, name='pokemon_query'),
]
