from django.contrib import admin

# Register your models here.
from app.models import EnterpriseType

register_admin = admin.site.register


class EnterpriseTypeAdmin(admin.ModelAdmin):
    model = EnterpriseType
    ordering = ['id']
    list_display = ['type', ]
    fields = ['type', ]


register_admin(EnterpriseType, EnterpriseTypeAdmin)
