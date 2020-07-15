from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import TripLinkerAccountManager


class TripLinkerAccountModel(AbstractBaseUser, PermissionsMixin):

    COUNTRIES = [("BY", "Belarus")]

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
    ]

    HOBBIES = [
        ("football", "Playing football"),
    ]

    # Base fields	
    first_name = models.CharField("First name", max_length=15, null=False)
    second_name = models.CharField("Second name", max_length=15, null=False)
    email = models.EmailField("E-mail", unique=True, null=False)
    sex = models.CharField("Sex", max_length=2, choices=SEX_CHOICES)
    date_of_birth = models.DateField("Date of birth", null=False)
    country = models.CharField("Country", max_length=25, choices=COUNTRIES)
    place_of_work = models.DateField("Place of work", null=True)
    short_description = models.CharField("Short description",max_length=500, 
    	null=True) 
    hobbies = models.CharField("Hobbies", max_length=250, null=True)

    # Social networks links
    vkontakte = models.URLField(verbose_name="VKontakte")
    twitter = models.URLField(verbose_name="Twitter")
    facebook = models.URLField(verbose_name="Facebook")

    # Special fields
    date_joined = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(verbose_name ="admin", default=False)
    is_active = models.BooleanField(verbose_name = "active",default=True)
    is_staff = models.BooleanField(verbose_name ="staff",default=False)


    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','second_name', 'sex', 'date_of_birth',
   		'country', 'password']


    objects = TripLinkerAccountManager()

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

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
