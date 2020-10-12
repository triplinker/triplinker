# Django modules.
from django.contrib import admin

# Current app modules.
from .models import Place, Photo, Feedback


admin.site.register(Place)
admin.site.register(Photo)
admin.site.register(Feedback)
