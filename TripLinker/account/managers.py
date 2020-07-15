from django.db import models
from django.contrib.auth.models import BaseUserManager


class TripLinkerAccountManager(BaseUserManager):

    def create_user(self, first_name, second_name, email, sex, country, 
                    date_of_birth, password):

        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.second_name = second_name
        user.sex = sex
        user.country = country
        user.date_of_birth = date_of_birth
        user.is_active = True
        user.is_staff = False
        user.is_admin = False
        user.is_superuser = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, second_name, email, sex,
                        date_of_birth, country, password):
        user = self.model(
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.second_name = second_name
        user.sex = sex
        user.country = country
        user.date_of_birth = date_of_birth
        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user