from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from sailoonapp.manager import UserManager 

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=12,null=True,blank=True)
    mobile_no = models.IntegerField(null=True,blank=True)
    deactivated_at = models.DateTimeField(auto_created=True,null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=True)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    otp_code = models.CharField(max_length=6,null=True,blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(auto_now=True)

class BusinessListing(models.Model):
    CATEGORY_CHOICES = [('saloon', 'Saloon'),('restaurant', 'Restaurant')]           
    business_name = models.CharField(max_length=140,null=True,blank=True) 
    address = models.TextField(null=True,blank=True) 
    business_contact = models.CharField(max_length=13,null=True,blank=True) 
    business_email = models.EmailField(unique=True,null=True,blank=True) 
    category_choice = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True) 
    business_description = models.TextField(null=True,blank=True) 
    operatint_hours = models.CharField(max_length=150,null=True,blank=True) 
    business_location = models.CharField(max_length=150,null=True,blank=True) 
    website = models.URLField(blank=True, null=True)  
    facebook_link = models.URLField(blank=True, null=True)  
    twitter_link = models.URLField(blank=True, null=True)  
    instagram_link = models.URLField(blank=True, null=True) 
    distance = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.business_name 

class ShopListing(models.Model): # saloon details 
    shop_schedule = models.CharField(max_length=250,null=True,blank=True)
    ratings = models.CharField(max_length=200,null=True,blank=True) 
    comments = models.CharField(max_length=200,null=True,blank=True) 
    near_by_shops = models.CharField(max_length=200,null=True,blank=True) 

    
class HaircutBoy(models.Model): # details of boy who wants go to saloon for cut hair & beard saving 
    name = models.CharField(max_length=29,null=True,blank=True) 
    # email = models.EmailField(unique=True,null=True,blank=True) 
    mobile_number = models.CharField(max_length=13,null=True,blank=True) 


class AppointmentCustomer(models.Model):
    customer_name = models.CharField(max_length=100,blank=True,null=True)
    visit_date_and_time = models.DateTimeField(auto_created=True,blank=True,null=True)
    service = models.CharField(max_length=100,null=True,blank=True) 


class Advertisement(models.Model): # user or business_saloon create advertisment 
    target_catogery = [('age','age'),('range','range'),('location','location')]
    age = models.CharField(max_length=200,null=True,blank=True)
    range = models.CharField(max_length=100,null=True,blank=True)
    title = models.CharField(max_length=200,null=True,blank=True) 
    description = models.CharField(max_length=200,null=True,blank=True) 
    image = models.ImageField(upload_to='images/',null=True,blank=True) 
    start_date = models.DateField(auto_created=True,blank=True,null=True) 
    end_date = models.DateField(auto_created=True,blank=True,null=True) 
    target_audience = models.CharField(max_length=200,choices=target_catogery,null=True,blank=True)
    location = models.CharField(max_length=200,null=True,blank=True) 

