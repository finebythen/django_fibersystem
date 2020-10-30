from django.contrib import admin
from .models import *


admin.site.register(Customer)
admin.site.register(Project)
admin.site.register(Cluster)

admin.site.register(IES)
admin.site.register(RohrTyp)
admin.site.register(EinzelrohrTyp)
admin.site.register(Kabel)
admin.site.register(Rohr)
admin.site.register(Hausanschlussrohr)
admin.site.register(Wohneinheit)

admin.site.register(Technikstandort)
admin.site.register(TechnikstandortDefault)
admin.site.register(Schacht_Kvz)
