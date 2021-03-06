# Django modules.
from django.contrib import admin

# !Triplinker modules

# Current app modules.
from .models.TLAccount_frequest import (TLAccount, FriendRequest,
                                        AvatarTLAccount, PersonalQualities)
from .forms.forms import UserCreationForm, UserChangeForm

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
                 'country', 'qualities'
                 )
        }
         ),

        ('Additional information', {
            'fields':
                ('place_of_work', 'short_description', 'hobbies', 'motto',
                 'date_joined',
                 )
        }
         ),

        ('Social networks', {
            'fields':
                ('vkontakte', 'twitter', 'facebook',)
        }
         ),

        (None, {'fields': ('can_get_message_from',)}),

        (None, {'fields': ('friends', 'followers', 'people_which_follow')}),

        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_admin')}),

        ('Password', {'fields': ('password',)}),
    )

    search_fields = ('first_name', 'second_name', 'email',)
    ordering = ('email',)
    readonly_fields = ('date_joined',)


admin.site.register(TLAccount, TLAccountAdmin)
admin.site.register(FriendRequest)
admin.site.register(AvatarTLAccount)
admin.site.register(PersonalQualities)
