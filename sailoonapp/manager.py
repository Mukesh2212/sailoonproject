from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager 
from django.db import models 

class UserManager(BaseUserManager):
    use_in_migrations = True 

    def create_user(self,email, password=None, **extra_fields):
        if not email:
            raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 


    def create_superuser(self,email, password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        # user = self.create_user(email, 
        #                         password = password,
        #                         )
        # user.is_admin = True
        # user.save(using=self._db)
        # return user

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Super user must have is_staff'))
        return self.create_user(email,password,**extra_fields) 












# class UserManager(BaseUserManager):
#     def create_user(self, email, name, mobile_no, password=None):
#         if not email:
#             raise ValueError("Users must have an email address")
#         if not name:
#             raise ValueError("Users must have a name")

#         user = self.model(
#             email=self.normalize_email(email),
#             name=name,
#             mobile_no=mobile_no,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, name, mobile_no, password=None):
#         user = self.create_user(
#             email=email,
#             name=name,
#             mobile_no=mobile_no,
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# class User(AbstractBaseUser):
#     email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     mobile_no = models.CharField(max_length=15, unique=True)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email

#     def has_perm(self, perm, obj=None):
#         return True

#     def has_module_perms(self, app_label):
#         return True

#     @property
#     def is_staff(self):
#         return self.is_admin