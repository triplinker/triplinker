from django.contrib import admin
from .models import TLAccount, FriendRequest
from .forms import UserCreationForm, UserChangeForm

admin.site.site_header = "TripLinker admin panel"


class TLAccountAdmin(admin.ModelAdmin):
    add_form = UserCreationForm
    form = UserChangeForm

    model = TLAccount

    list_display = (
        'first_name', 'second_name', 'email', 'sex', 'date_of_birth',
        'country', 'is_active', 'is_staff', 'is_admin',
    )

    list_filter = ('sex', 'date_of_birth', 'is_admin', 'is_staff', 'is_active',
                   'hobbies',
                   )

    fieldsets = (
        ('Main information', {
            'fields':
                ('first_name', 'second_name', 'email', 'sex', 'date_of_birth',
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

        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),

        (None, {'fields': ('friends',)}),

        ('Password', {'fields': ('password',)}),
    )

    search_fields = ('first_name', 'second_name', 'email',)
    ordering = ('email',)
    readonly_fields = ('date_joined',)


admin.site.register(TLAccount, TLAccountAdmin)
admin.site.register(FriendRequest)
