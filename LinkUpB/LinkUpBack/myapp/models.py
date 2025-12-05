from django.db import models
from django.contrib.auth.models import User

class profils(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=[('seeker', 'Job Seeker'), ('company', 'Company')])

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
class people(models.Model):
    Id_Profil = models.ForeignKey(profils, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.Id_Profil.user.username} - {self.age} years"

    def __unicode__(self):
        return "{0} [{1}]".format(self.Id_Profil, self.age)
    
class companies(models.Model):
    Id_Profil = models.ForeignKey(profils, on_delete=models.CASCADE)
    companie_name = models.CharField(max_length=100)
    place = models.CharField(max_length=100) 
    description = models.CharField(max_length=300)
 
    def __str__(self):
        return f"{self.Id_Profil.user.username} - {self.place}"

    def __unicode__(self):
        return "{0} {1} [{2}]".format(self.Id_Profil, self.place, self.description)

class advertisements(models.Model):
    Id_Profil = models.ForeignKey(companies, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    short_description = models.CharField(max_length=300)
    long_description = models.TextField()
    salary = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    schredule = models.CharField(max_length=100)
    
class applications(models.Model):
    Id_Profil = models.ForeignKey(people, on_delete=models.CASCADE)
    Id_Job = models.ForeignKey(advertisements, on_delete=models.CASCADE)
    accept = models.BooleanField(null=True)
    message = models.CharField(max_length=300)