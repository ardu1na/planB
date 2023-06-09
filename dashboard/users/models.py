from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from django.contrib.auth.models import Group




class CustomAccountManager(BaseUserManager):
	
	def create_superuser(self, email,   password,**other_fields):
		other_fields.setdefault('is_staff',True)
		other_fields.setdefault('is_superuser',True)
		other_fields.setdefault('is_active',True)
		if other_fields.get('is_staff') is not True:
			raise ValueError(
				'Superuser must be assigned to is_staff=True.')
		if other_fields.get('is_superuser') is not True:
			raise ValueError(
				'Superuser must be assigned to is_superuser=True.')
		super_user = self.create_user(email, password, **other_fields)
		return super_user

	def create_user(self, email,  password,**other_fields):
		
		if not email:
			raise ValueError(_('You must provide an email address'))
		email = self.normalize_email(email)
		user = self.model(email=email,  **other_fields)
		user.set_password(password)
		user.save()
		return user



class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'),unique=True)
	username = models.CharField(blank=True, max_length=50)
 
	
	def save (self, *args, **kwargs):
		if self.username is None:
			self.username = self.email.replace('@', '')

		super().save(*args, **kwargs)  
			
			
	groups = models.ManyToManyField(Group,blank=True)
	
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=False)
	
	objects = CustomAccountManager()

	USERNAME_FIELD = 'email'  
 

	


	def __str__(self):
		return str(self.email)

	class Meta:
 		ordering = ['email',]