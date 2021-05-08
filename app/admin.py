from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

class ProfileInline(admin.StackedInline):
    model = CHPuser
    can_delete = False
    verbose_name_plural = 'Staff Number'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )
    list_display = ('username', 'get_staff_number', 'first_name', 'last_name', 'email')
    list_select_related = ('chpuser', )

    def get_staff_number(self, instance):
        return instance.chpuser.staff_number
    get_staff_number.short_description = 'Staff Number'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Register your models here.
admin.site.register(Case)
admin.site.register(Event)