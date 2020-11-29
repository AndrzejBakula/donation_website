from django.contrib import admin
from portfolio_app.models import Institution

class InstitutionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Institution, InstitutionAdmin)
