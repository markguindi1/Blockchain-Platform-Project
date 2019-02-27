"""blockchainplatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', include('bcplatform.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('user_accounts.urls')),

    # In the admin files, the "password_change_done" view is linked to without an app namespace, so the entire url
    # would be /password-change-done/ instead of /user/password-change-done/ (and the name of the url would be just
    # password_change_done instead of user_accounts:password_change_done), so I needed to list that path here. The
    # below path redirects it to the correct view in the user_accounts app.
    path('password-change-done/', RedirectView.as_view(pattern_name="user_accounts:password_change_done"),
         name="password_change_done"),

]
