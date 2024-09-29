from django.contrib import admin
from sailoonapp.models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email','name','mobile_no','deactivated_at','is_active','is_superuser','is_staff']
    

@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ['user','otp_code','created_at','expiration_time']
    

@admin.register(BusinessListing)
class BusinessListingAdmin(admin.ModelAdmin):
    list_display = ['id','business_name','address','business_contact','business_email',
                    'category_choice','business_description','operatint_hours','business_location',
                    'website','facebook_link','twitter_link','instagram_link','distance']


@admin.register(ShopListing)
class ShopListingAdmin(admin.ModelAdmin):
    list_display = ['id','shop_schedule','ratings','comments','near_by_shops']
    
@admin.register(HaircutBoy)
class HaircutBoyAdmin(admin.ModelAdmin):
    list_display = ['id','name','mobile_number']
    
@admin.register(AppointmentCustomer)
class AppointmentCustomerAdmin(admin.ModelAdmin):
    list_display = ['id','customer_name','visit_date_and_time','service']


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','image','start_date','end_date','target_audience','age','range','location']
    
