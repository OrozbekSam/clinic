from django.contrib import admin
from doctor.models import Doctor, Medicine, Favorite

admin.site.register(Doctor)
admin.site.register(Medicine)
admin.site.register(Favorite)