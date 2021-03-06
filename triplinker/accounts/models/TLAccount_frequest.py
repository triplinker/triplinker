# Python modules.
import datetime

# Another project modules.
import django_filters

# Django modules.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db.models import Q
from django_filters.widgets import RangeWidget

# !Triplinker modules:

# Current app module.
from accounts.managers import TLAccountManager


class PersonalQualities(models.Model):
    """Adds the possibility to create qualities for the field 'qualities' of
       TLAccount model."""
    quality = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.quality}'

    class Meta:
        verbose_name = 'Quality'
        verbose_name_plural = 'Qualities'


class TLAccount(AbstractBaseUser, PermissionsMixin):
    """Main model in project.
    Model contains basic fields which are connected with user's info
    This is key model for Post and Comment models.
    """
    COUNTRIES = [("BY", "Belarus")]

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    HOBBIES = [
        ("football", "Playing football"),
    ]

    CAN_GET_MSSGES_FROM_CHOICES = [
        ("Friends", "Friends only"),
        ("All", "All users"),
    ]

    # Base fields
    first_name = models.CharField("First name", max_length=15, blank=True)
    second_name = models.CharField("Second name", max_length=15, blank=True)
    email = models.EmailField("E-mail", unique=True)
    sex = models.CharField("Sex", max_length=2, choices=SEX_CHOICES, blank=True)
    date_of_birth = models.DateField("Date of birth", blank=True, null=True)
    country = models.CharField("Country", max_length=25, choices=COUNTRIES,
                               blank=True)
    qualities = models.ManyToManyField(PersonalQualities, blank=False)

    # Additional information about user
    place_of_work = models.CharField("Place of work", max_length=70, blank=True)
    short_description = models.CharField("Short description", max_length=500,
                                         blank=True)
    hobbies = models.CharField("Hobbies", max_length=250, blank=True)
    motto = models.CharField("Motto", max_length=62, blank=True, null=True)

    # Social networks links
    vkontakte = models.URLField(verbose_name="VKontakte", blank=True, null=True)
    twitter = models.URLField(verbose_name="Twitter", blank=True, null=True)
    facebook = models.URLField(verbose_name="Facebook", blank=True, null=True)

    # Friends system
    friends = models.ManyToManyField("TLAccount", blank=True)

    # Users who follow current user.
    followers = models.ManyToManyField("TLAccount", blank=True,
                                       related_name='followers_of_user')

    # Users who are being followed by current user
    rl_name = 'people_which_follow_cur_usr'  # For variable->people_which_follow
    people_which_follow = models.ManyToManyField("TLAccount", blank=True,
                                                 related_name=rl_name)

    # Messages
    can_get_message_from = models.CharField("Get messages from",
                                            max_length=12,
                                            choices=CAN_GET_MSSGES_FROM_CHOICES,
                                            blank=False, default='All')

    # Users which are not friends of user but they can send messages to him,
    strangers = models.ManyToManyField("TLAccount", blank=True,
                                       related_name='messages_strangers')
    # Special fields
    date_joined = models.DateTimeField(verbose_name="Date joined",
                                       default=timezone.now)
    is_admin = models.BooleanField(verbose_name="admin", default=False)
    is_active = models.BooleanField(verbose_name="active", default=True)
    is_staff = models.BooleanField(verbose_name="staff", default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name', 'sex',
                       'date_of_birth', 'country', 'password']

    # Custom model manager
    objects = TLAccountManager()

    def __str__(self):
        return self.email

    def get_age(self):
        """Helps to find out the age of a user according to his date of
        birth."""
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)

    def is_birthday(self):
        """Helps to find out if user has birthday on the day when the
        method was called."""

        todays_date = str(datetime.date.today())[5:]
        birth_date = str(self.date_of_birth)[5:]

        if todays_date == birth_date:
            return True
        else:
            return False

    def flavor_verbose(self):
        """Returns full value in tuples of CHOICES"""
        return dict(TLAccount.COUNTRIES)[self.country]

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class AvatarTLAccount(models.Model):
    """Gives the possibility of storying an avatar of an user."""
    rlted_name = 'get_avatar'
    user = models.ForeignKey(TLAccount,  on_delete=models.CASCADE,
                             related_name=rlted_name, blank=True, null=True)
    profile_image = models.ImageField('Profile image',
                                      upload_to='accounts/user_main_photo')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Avatar of {self.user}'

    class Meta:
        verbose_name = 'AvatarTLAccount'
        verbose_name_plural = 'AvatarsTLAccounts'


class UserPhotoGallery(models.Model):
    """Gives the possibility to store user's photos from his gallery."""
    photo = models.ImageField('Photos of place',
                              upload_to='accounts/user_gallery',
                              null=True, blank=True)

    author = models.ForeignKey(TLAccount, related_name='photos_of_user',
                               blank=True, null=True, default=None,
                               on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "Author: {}, Photo: {}".format(self.author, self.photo)

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'UserPhoto (Gallery)'
        verbose_name_plural = 'UserPhotos (Gallery)'


class UserFilter(django_filters.FilterSet):
    """Filtier for finding user(s) from the page with all_users (People)."""
    q = django_filters.CharFilter(
        method='full_name_filter',
        label='Name')
    age = django_filters.RangeFilter(
        method='age_filter',
        widget=RangeWidget,
        label='Age')

    class Meta:
        model = TLAccount
        fields = ['q', 'sex', 'age', 'country']

    def full_name_filter(self, queryset, name, value):
        return queryset.filter(Q(first_name__icontains=value) |
                               Q(second_name__icontains=value) |
                               Q(email__icontains=value))

    def age_filter(self, queryset, name, value):
        if value.stop is not None:
            birth_after = (datetime.date.today() - datetime.timedelta(
                days=float(value.stop)*365.25))
            queryset = queryset.filter(date_of_birth__gte=birth_after)
        if value.start is not None:
            birth_before = (datetime.date.today() - datetime.timedelta(
                days=float(value.start)*365.25))
            queryset = queryset.filter(date_of_birth__lte=birth_before)
        return queryset


class FriendRequest(models.Model):
    """Model for storing friend requests between users."""
    from_user = models.ForeignKey(TLAccount,
                                  related_name='from_user',
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(TLAccount,
                                related_name='to_user',
                                on_delete=models.CASCADE)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.email, self.to_user.email)

    class Meta:
        verbose_name = 'Friend request'
        verbose_name_plural = 'Friend requests'
