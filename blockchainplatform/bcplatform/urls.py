"""application_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, reverse_lazy
from . import views

app_name = 'bcplatform'

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('blockchain/', views.RedirectView.as_view(url=reverse_lazy("bcplatform:homepage"))),
    path('blockchain/create/', views.BlockchainCreateView.as_view(), name='blockchain_create'),
    path('blockchain/<int:pk>/', views.BlockchainDetailView.as_view(), name='blockchain_detail_view'),
    path('blockchain/<int:pk>/update/', views.BlockchainUpdateView.as_view(), name='blockchain_update_view'),
    path('blockchain/<int:pk>/delete/', views.BlockchainDeleteView.as_view(), name='blockchain_delete_view'),
    path('blockchain/<int:bc_pk>/create-block/', views.BlockCreateView.as_view(), name='block_create_view'),
    path('blockchain/<int:bc_pk>/corrupt-blockchain/', views.BlockchainCorruptFormView.as_view(), name='blockchain_corrupt_form_view'),
]
