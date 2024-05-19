"""
URL configuration for support project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.autorisation_view),
    path('auth', views.post_authorisation),
    path('chose-role', views.chose_role_page_view),
    path('tickets', views.tickets_view),
    path('create-ticket', views.user_create_ticket_page),
    path('get-user-ticket', views.get_user_ticket),
    path('user-tickets', views.user_tickets),
    path('tickets-list', views.tickets_list_view),
    path('get-user-tickets-list', views.get_user_tickets_list),
    path('get-category-custom-attribute', views.get_category_custom_attribute),
    path('watch-ticket/<id>', views.open_ticket_support)
]
