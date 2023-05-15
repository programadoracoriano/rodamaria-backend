from django.contrib import admin
from .models import *
# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    model           = Profile
    list_display    = ('id',)
    search_fields   = ('id','name', )

class BikeAdmin(admin.ModelAdmin):
    model           = Bike
    list_display    = ('id',)
    search_fields   = ('id','name', )

class PlanAdmin(admin.ModelAdmin):
    model           = Plan
    list_display    = ('id',)
    search_fields   = ('id','name', )

class RentAdmin(admin.ModelAdmin):
    model           = Rent
    list_display    = ('id',)
    search_fields   = ('id', )

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Bike, BikeAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Rent, RentAdmin)
