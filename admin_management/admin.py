# admin.py in the respective app

from django.contrib import admin
from .models import AdminActions

class CustomAdminActionsAdmin(admin.ModelAdmin):
    list_display = ('service', 'status', )
    list_filter = ('service', 'status', )
    
    def has_add_permission(self, request):
        return False
      

admin.site.register(AdminActions, CustomAdminActionsAdmin)
