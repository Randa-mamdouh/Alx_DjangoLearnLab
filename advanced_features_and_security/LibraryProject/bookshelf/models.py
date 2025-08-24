from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE, ManyToManyField, OneToOneField, Foreign
from django.db.models import Model, CharField
from django.contrib.auth.models import AbstractUser, BaseUserManager    
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import IntegerField, ImageField

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100, on_delete=models.CASCADE, related_name='books')
    publishing_year = IntegerField()

def __str__(self):
        return self.title



class CustomUserManager(BaseUserManager):

    class Meta:
        permission = [(
        ("can_view", "view_book"),
        ("can_create", "create_book"),
        ("can_delete", "delete_book"),
        )]
    def create_superuser(self, email, password=None, date_of_birth=None, profile_photo=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
        email = self.normalize_email(email),
        date_of_birth = date_of_birth,
        profile_photo = profile_photo
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None, date_of_birth=None, profile_photo=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            profile_photo=profile_photo
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_admin = models.BooleanField(default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = 'date_of_birth', 'profile_photo'


# create groups
editors_group, created = Group.objects.get_or_create(name='Editors')
viewers_group, created = Group.objects.get_or_create(name='Viewers')
admins_group, created = Group.objects.get_or_create(name='Admins')

# assign permissions to groups
can_edit_permission = Permission.objects.get(codename='can_edit')
can_create_permission = Permission.objects.get(codename='can_create')
can_view_permission = Permission.objects.get(codename='can_view')  
can_delete_permission = Permission.objects.get(codename='can_delete')

editors_group.permissions.add(can_edit_permission, can_create_permission)
viewers_group.permissions.add(can_view_permission)
admins_group.permissions.add(can_edit_permission, can_create_permission, can_view_permission, can_delete_permission)



    




