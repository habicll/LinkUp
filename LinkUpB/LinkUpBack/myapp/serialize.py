from rest_framework import serializers
from rest_framework import serializers
from .models import profils
from .models import people
from .models import companies
from .models import advertisements
from .models import applications


class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = profils
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='Id_Profil.user.email', read_only=True)
    class Meta:
        model = people
        fields = ['Id_Profil', 'name', 'age', 'email']


class CompanySerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='Id_Profil.user.email', read_only=True)
    class Meta:
        model = companies
        fields = ['Id_Profil', 'companie_name', 'place', 'description', 'email']
        read_only_fields = ('email',)



class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = advertisements
        fields = ['id','Id_Profil','title','short_description','long_description','salary','start_date','end_date','schredule']


class ApplicationSerializer(serializers.ModelSerializer):
    company_id = serializers.SerializerMethodField()
    name = serializers.CharField(source='Id_Profil.name', read_only=True)
    Id_Profil = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = applications
        fields = ['Id_Job', 'accept', 'message', 'Id_Profil', 'company_id', 'name', 'id']
        read_only_fields = ('Id_Profil', 'name')

    def create(self, validated_data):
        user = self.context['request'].user
        try:
            profil = profils.objects.get(user=user)
            person = people.objects.get(Id_Profil=profil)
        except people.DoesNotExist:
            raise serializers.ValidationError("This user is not a person/seeker.")

        validated_data['Id_Profil'] = person
        application = applications.objects.create(
            **validated_data
        )
        return application

    def get_company_id(self, obj):
        try:
            company = obj.Id_Job.Id_Profil
            return company.id if company else None
        except AttributeError:
            return None


from dj_rest_auth.serializers import TokenSerializer
from rest_framework import serializers as _rest_serializers
from .models import profils, people, companies


class CustomTokenSerializer(TokenSerializer):
    user_type = _rest_serializers.CharField(source="user.profils.user_type", read_only=True)
    profile_id = _rest_serializers.IntegerField(source="user.profils.id", read_only=True)
    seeker_id = _rest_serializers.SerializerMethodField()
    company_id = _rest_serializers.SerializerMethodField()

    class Meta(TokenSerializer.Meta):
        fields = TokenSerializer.Meta.fields + (
            'user_type',
            'profile_id',
            'seeker_id',
            'company_id',
        )

    def get_seeker_id(self, obj):
        person = people.objects.filter(Id_Profil=obj.user.profils).first()
        return person.id if person else None

    def get_company_id(self, obj):
        company = companies.objects.filter(Id_Profil=obj.user.profils).first()
        return company.id if company else None
