from rest_framework import serializers 
from django.contrib.auth import get_user_model 
from sailoonapp.models import *
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken ,  TokenError
import re

User = get_user_model() 


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User 
        fields = "__all__"

    def validate_password(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Password must be at least 10 characters long. At least one uppercase letter ,At least one special character")
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Password must be at least 10 characters long. At least one uppercase letter ,At least one special character")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must be at least 10 characters long. At least one uppercase letter ,At least one special character")
        
        return value
    
    def create(self, validated_data):
        user = User(
            name=validated_data['name'],
            email=validated_data['email'],
            mobile_no=validated_data['mobile_no']
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['otp_code']


class BusinessListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessListing 
        fields = ['business_name','address','business_contact','business_email',
                    'category_choice','business_description','operatint_hours','business_location',
                    'website','facebook_link','twitter_link','instagram_link','distance'] 
        

    def validate_business_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Business name must start with a capital letter.")
        
        # # Ensure the business name is unique
        # if BusinessListing.objects.filter(business_name=value).exists():
        #     raise serializers.ValidationError("A business with this name already exists.")
        
        return value

    def validate_business_contact(self, value):
        if not value.startswith('+91'):
            raise serializers.ValidationError("Business contact number must start with the country code +91.")
        if len(value) != 13:  
            raise serializers.ValidationError("Business contact number must be 13 characters long, including the country code.")
        return value

    def validate_business_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid email address.")
        return value 
    
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopListing
        fields = ['id', 'shop_schedule', 'ratings', 'comments', 'near_by_shops']

    def validate_id(self, value):
        """
        Check if the provided id exists in the database.
        """
        if not ShopListing.objects.filter(id=value).exists():
            raise serializers.ValidationError("No shop found with the provided ID.")
        return value 
    
class RatcomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopListing
        fields = ['id',  'ratings', 'comments']

    def validate_id(self, value):
        """
        Check if the provided id exists in the database.
        """
        if not ShopListing.objects.filter(id=value).exists():
            raise serializers.ValidationError("No shop found with the provided ID.")
        return value 
    
class HaircutSerializer(serializers.ModelSerializer):
    class Meta:
        model = HaircutBoy 
        fields = ['id','name','mobile_number'] 
    
    def validate_mobile_number(self,value):
        if not value.startswith('+91'):
            raise serializers.ValidationError("Business contact number must start with the country code +91.")
        if len(value) !=13:
            raise serializers.ValidationError("Business contact number must be 13 characters long, including the country code.")
        return value 
    
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentCustomer
        fields = ['id','customer_name','visit_date_and_time','service'] 

    def validate_id(self, value):
        """
        Check if the provided id exists in the database.
        """
        if not AppointmentCustomer.objects.filter(id=value).exists():
            raise serializers.ValidationError("No shop found with the provided ID.")
        return value 
    

class AdvertismentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = ['id','title','description','image','start_date','end_date','target_audience','age','range','location']

    def validate_title(self,value):
        if not value.strip():
            raise serializers.ValidationError('Title can not be empty')
        return value    
    
    def validate_description(self,value):
        max_length = 500 
        if len(value) > max_length:
            raise serializers.ValidationError(f"Description cannot exceed {max_length} characters.") 
        return value 
    


# class ChangePasswordSerializer(serializers.Serializer):
#     email= serializers.EmailField()
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if new_password != confirm_new_password:
            raise serializers.ValidationError("New password and confirm new password do not match.")
        return data

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField() 
    default_error_messages = {
        'bad_token':'Token is expiered or Invalid '
    }
    def validate(self,attrs):
        self.tokent = attrs['refresh'] or attrs.get('refresh')
        return attrs 
    def save(self,**kwargs):
        try:
            RefreshToken(self.tokent).blacklist()
        except TokenError :
            self.fail('bad_token')

