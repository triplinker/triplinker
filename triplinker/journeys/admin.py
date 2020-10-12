# Django modules.
from django.contrib import admin

# !Triplinker modules:

# Current app modules.
from .models import Journey, Participant, Activity


admin.site.register(Journey)
admin.site.register(Participant)
admin.site.register(Activity)
