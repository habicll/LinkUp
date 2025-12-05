from django.contrib import admin
from .models import profils
admin.site.register(profils)
from .models import advertisements
admin.site.register(advertisements)
from .models import companies
admin.site.register(companies)
from .models import applications
admin.site.register(applications)
from .models import people
admin.site.register(people)