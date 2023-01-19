from django.contrib import admin
from .models import Institution, Donation, Category

admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(Donation)
