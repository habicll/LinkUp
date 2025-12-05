from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from dj_rest_auth.views import LoginView
from rest_framework.views import APIView



from .models import profils, people, companies, advertisements, applications
from .serialize import ProfilSerializer, PersonSerializer, CompanySerializer, AdvertisementSerializer, ApplicationSerializer, CustomTokenSerializer

class ProfilViewSet(viewsets.ModelViewSet):
    queryset = profils.objects.all()
    serializer_class = ProfilSerializer
    
class PersonViewSet(viewsets.ModelViewSet):
    queryset = people.objects.all()
    serializer_class = PersonSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = companies.objects.all()
    serializer_class = CompanySerializer
    

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = advertisements.objects.all()
    serializer_class = AdvertisementSerializer

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = applications.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]


class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()
        token_serializer = CustomTokenSerializer(instance=self.token)
        response.data.update(token_serializer.data)
        return response

    
from dj_rest_auth.registration.views import RegisterView

class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        user = serializer.save(self.request)
        user_type = self.request.data.get('user_type')
        name = self.request.data.get('name')
        companie_name = self.request.data.get('companie_name')
        age = self.request.data.get('age')
        place = self.request.data.get('place')
        description = self.request.data.get('description')

        profil = profils.objects.create(user=user, user_type=user_type)

        if user_type == 'seeker':
            people.objects.create(Id_Profil=profil, name=name, age=age)
        elif user_type == 'company':
            companies.objects.create(Id_Profil=profil, companie_name=companie_name, place=place, description=description)
        try:
            from rest_framework.authtoken.models import Token
            Token.objects.get_or_create(user=user)
        except Exception:
            pass

        return user
    

class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()  # cascade supprime profil, company, ads, etc.
        return Response({"message": "Account deleted successfully."}, status=204)
