from django.contrib import admin

from .models import Category, Donation, Institution

admin.site.register([Category, Institution, Donation])
