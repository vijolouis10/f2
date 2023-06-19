from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, phone_number, password=None):
        if not email:
            raise ValueError("User must have an Email Address")

        if not username:
            raise ValueError("User must have an Username")

        user = self.model(

            first_name   =  first_name,
            last_name    =  last_name,
            username     =  username,
            email        =  self.normalize_email(email),
            phone_number =  phone_number
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, phone_number, password):

        user = self.create_user(

            email        =  self.normalize_email(email),
            username     =  username,
            first_name   =  first_name,
            last_name    =  last_name,
            password     =  password,
            phone_number =  phone_number
        )

        user.is_admin    =  True
        user.is_active   =  True
        user.is_staff    =  True
        user.is_superadmin    =  True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
   
    first_name     =  models.CharField(max_length=40)
    last_name      =  models.CharField(max_length=40) 
    username       =  models.CharField(max_length=40, unique=True)
    email          =  models.EmailField(max_length=70, unique=True)
    phone_number   =  models.CharField(max_length=50)

    #REQUIRED

    date_joined    =  models.DateTimeField(auto_now_add=True)
    last_login     =  models.DateTimeField(auto_now_add=True)
    is_admin       =  models.BooleanField(default=False)
    is_staff       =  models.BooleanField(default=False)
    is_active      =  models.BooleanField(default=False)
    is_superadmin  =  models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone_number']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
class UserProfile(models.Model):
  user=models.OneToOneField(Account,on_delete=models.CASCADE)
  address_line_1=models.CharField(max_length=100,blank=True)
  address_line_2=models.CharField(max_length=100,blank=True)
  profile_pic=models.ImageField(blank=True,upload_to='photos/profile_pic',default='photo/profile_pic/default.jpg')
  city=models.CharField(max_length=20,blank=True)
  pincode=models.CharField(null=True,max_length=6)
  state=models.CharField(max_length=20,blank=True)
  country=models.CharField(max_length=20,blank=True)
  
  def __str__(self):
      return self.user.first_name

  def full_address(self):
    return self.address_line_1+" "+self.address_line_2    


class Otp(models.Model):
  user=models.ForeignKey(Account,on_delete=models.CASCADE)
  otp=models.IntegerField()

  def __str__(self):
    return str(self.otp)