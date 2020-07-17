from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TLAccount
from .forms import UserCreationForm, UserChangeForm


admin.site.site_header = "TripLinker admin panel"


class TLAccountAdmin(admin.ModelAdmin):
	add_form = UserCreationForm
	form = UserChangeForm

	model = TLAccount

	list_display = ('first_name','second_name', 'email', 'sex', 'date_of_birth',
		'country', 'is_active', 'is_staff', 'is_admin',
	)

	list_filter = ('sex', 'date_of_birth', 'is_admin', 'is_staff', 'is_active',
		'hobbies',
	)

	fieldsets = (
		('Main information', {
			'fields': 
				('first_name', 'second_name','email','sex','date_of_birth',
					'country',
				)
			}
		),

		('Additional information', {
			'fields': 
				('place_of_work', 'short_description', 'hobbies', 'date_joined'
				)
			}
		),

		('Social networks', {
			'fields': 
				('vkontakte', 'twitter', 'facebook',)
			}
		),

		('Permissions', {'fields': ('is_active','is_staff', 'is_admin')}),

		('Passwords', {'fields': ('password1', 'password2')}),
	)

	search_fields = ('first_name', 'second_name', 'email',)
	ordering = ('email',)
	readonly_fields = ('date_joined',)

admin.site.register(TLAccount, TLAccountAdmin)