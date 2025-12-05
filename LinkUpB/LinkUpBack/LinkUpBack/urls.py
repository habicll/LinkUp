"""
URL configuration for LinkUpBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
# from django.contrib import admin
# from django.urls import path,include
# from myapp.endpoints import profils
# from myapp.endpoints import seekers
# from myapp.endpoints import compagnies
# from myapp.endpoints import jobs
# from myapp.endpoints import relations

# urlpatterns = [
#     path('admin', admin.site.urls),
#     path('Profils',profils.ReadProfils,name='ReadProfils'),
#     path('OneProfil/<int:pk>',profils.OneProfil,name='OneProfil'),
#     path('CreateProfils',profils.CreateProfil,name='CreateProfil'),
#     path('DeleteEntreprise',profils.DeleteProfil,name='DeleteProfil'),
    
#     path('Compagnies',compagnies.ReadCompagnies,name='ReadCompagnies'),
#     path('OneCompagny/<int:pk>',compagnies.OneCompagny,name='OneCompagny'),
    
#     path('Jobs',jobs.ReadJobs,name='ReadJobs'),
#     path('OneJob/<int:pk>',jobs.OneJob,name='OneJob'),
# ]



from django.contrib import admin
from django.urls import path, include
from myapp.views import CustomRegisterView, CustomLoginView, DeleteAccountView
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('dj-rest-auth/registration/', CustomRegisterView.as_view(), name='custom_register'),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('', include('myapp.urls')),  
    path('delete-account/', DeleteAccountView.as_view(), name='delete-account'),
]