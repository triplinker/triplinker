from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import TLAccountManager
import datetime


class TLAccount(AbstractBaseUser, PermissionsMixin):
    COUNTRIES = [("BY", "Belarus")]

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    HOBBIES = [
        ("football", "Playing football"),
    ]

    # Base fields
    first_name = models.CharField("First name", max_length=15, blank=True)
    second_name = models.CharField("Second name", max_length=15, blank=True)
    email = models.EmailField("E-mail", unique=True)
    sex = models.CharField("Sex", max_length=2, choices=SEX_CHOICES, blank=True)
    date_of_birth = models.DateField("Date of birth", blank=True, null=True)
    country = models.CharField("Country", max_length=25, choices=COUNTRIES,
                               blank=True)
    place_of_work = models.CharField("Place of work", max_length=70, blank=True,
                                     null=True)
    short_description = models.CharField("Short description", max_length=500,
                                         blank=True)
    hobbies = models.CharField("Hobbies", max_length=250, blank=True,
                               null=True)

    # Social networks links
    vkontakte = models.URLField(verbose_name="VKontakte", blank=True, null=True)
    twitter = models.URLField(verbose_name="Twitter", blank=True, null=True)
    facebook = models.URLField(verbose_name="Facebook", blank=True, null=True)

    # Friends system
    friends = models.ManyToManyField("TLAccount", blank=True)

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

    objects = TLAccountManager()

    def __str__(self):
        return self.email

    def get_age(self):
        return int((datetime.date.today() - self.date_of_birth).days / 365.25)

    def is_birthday(self):
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

    def get_all_posts(self):
        return self.post.all()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'


class FriendRequest(models.Model):
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
