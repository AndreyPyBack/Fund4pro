from django.contrib import admin
from .models import Investor, Businessman, InterestSector

admin.site.register(Investor)
admin.site.register(Businessman)
admin.site.register(InterestSector)
