from django.contrib.auth.models import BaseUserManager

from .helpers.manager.create_users_func import create_acc


class TLAccountManager(BaseUserManager):

    def create_user(self, first_name, second_name, email, sex,
                    date_of_birth, country, password, user_type="common_user"):
        user = self.model(
            email=self.normalize_email(email),
        )

        args = locals()
        class_instance = BaseUserManager()
        user_obj = create_acc(user, args, class_instance, user_type)
        return user_obj

    def create_superuser(self, first_name, second_name, email, sex,
                         date_of_birth, country, password):
        user_obj = self.create_user(first_name, second_name, email, sex,
                                    date_of_birth, country, password,
                                    user_type="super_user")
        return user_obj
