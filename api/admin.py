from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import (
    Profile, PetType, Pet, PetMedicalHistory,
    PetReport, PetAdoption, Notification
)
from django.contrib import admin
from .models import Profile, PetType, Pet, PetMedicalHistory, PetReport, PetAdoption, Notification

admin.site.register(Profile)
admin.site.register(PetType)
admin.site.register(Pet)
admin.site.register(PetMedicalHistory)
admin.site.register(PetReport)
admin.site.register(PetAdoption)
admin.site.register(Notification)
