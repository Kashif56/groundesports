from django.contrib import admin
from .models import Tournament, Teams, Contact, Payment

# Register your models here.
admin.site.register(Tournament)
admin.site.register(Teams)
admin.site.register(Payment)
admin.site.register(Contact)

