from rest_framework import routers
from myapp.views import ProfilViewSet, PersonViewSet, CompanyViewSet, AdvertisementViewSet, ApplicationViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register(r'profils', ProfilViewSet)
router.register(r'people', PersonViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'advertisements', AdvertisementViewSet)
router.register(r'applications', ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]