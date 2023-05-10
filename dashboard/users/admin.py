from django.contrib import admin
from dashboard.users.models import CustomUser
from django.contrib.auth.admin import UserAdmin



class UserAdminConfig(UserAdmin):
	model = CustomUser
	search_fields = ('email',)
	list_filter = ('email','is_active','is_staff')
	list_display=('email','is_active','is_staff')

	fieldsets=(
			(None,{'fields':('email', )}),
			('Permissions',{'fields':('is_staff','is_active','is_superuser','groups','user_permissions')}),
		)


	add_fieldsets = (
	(None,{
		'classes':('wide',),
		'fields':('email','password1','password2','is_active','is_staff','groups','user_permissions')
		}
		),
	)

admin.site.register(CustomUser,UserAdminConfig)

# Register your models here.
