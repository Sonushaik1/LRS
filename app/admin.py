from django.contrib import admin

# Register your models here.
from .models import Register,Landdetails,LandRequest,LandRegistration

admin.site.register(Register)
admin.site.register(Landdetails)
admin.site.register(LandRequest)
admin.site.register(LandRegistration)