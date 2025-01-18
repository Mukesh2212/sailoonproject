from django.shortcuts import render
from sailoonapp.serializer import *
from sailoonapp.models import *
from django.contrib.auth import get_user_model
from rest_framework.views  import APIView
from rest_framework import status , permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken , TokenError
import random 
from django.utils import timezone
from datetime import timedelta
from twilio.rest import Client
import os 
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail 
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate


class UserRegistrationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user is None:
            raise Exception("Error in creating new account") 
        return Response({f'{user}':"You have registered successfully "}, status=status.HTTP_201_CREATED)
    
TWILIO_ACCOUNT_SID = 'AC08cc9a04850e102beb72cf6b306dd699'
TWILIO_AUTH_TOKEN = 'a48d8a1faeaa6ded14699ad7aa99d763'
TWILIO_PHONE_NUMBER = '+19383566144'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_otp(phone_number,otp_code):
    """Send OTP to the specified phone number using Twilio."""
    message_body = f"Your OTP code is {otp_code}. Please do not share it with anyone."

    try:
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"OTP sent successfully: {message.sid}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# class LoginAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         phone_number = request.data.get('mobile_no')  
#         if not phone_number:
#             return Response({'error': 'Mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user = User.objects.filter(mobile_no=phone_number).first() 
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         otp_code = random.randint(100000,999999)
#         created_at = timezone.now()
#         expiration_time = timezone.now() + timedelta(minutes=1)  
#         OTP.objects.create(
#             user=user,
#             otp_code=otp_code,
#             created_at=created_at,
#             expiration_time=expiration_time
#         )
#         if send_otp(phone_number , otp_code):
#             return Response({'message': 'OTP sent to your mobile number'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')  
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.filter(email=email).first()
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        otp_code = random.randint(100000, 999999)
        created_at = timezone.now()
        expiration_time = created_at + timedelta(minutes=3)  # OTP valid for 3 minutes
        OTP.objects.create(
            user=user,
            otp_code=otp_code,
            created_at=created_at,
            expiration_time=expiration_time
        )
        email_subject = 'Your OTP Code'
        email_message = f'Your OTP code is {otp_code}. It will expire in 3 minutes.'
        if send_mail(email_subject, email_message, 'mk2648054@gmail.com', [email]):
            return Response({'message': 'OTP sent to your email address'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class VerifyOTPAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         mobile_no = request.data.get('mobile_no')
#         otp_code = request.data.get('otp_code')

#         if not mobile_no or not otp_code:
#             return Response({'error': 'Mobile number and OTP code are required'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user = User.objects.filter(mobile_no=mobile_no).first()
#             otp = OTP.objects.filter(user=user, otp_code=otp_code).latest('created_at')
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except OTP.DoesNotExist:
#             return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
#         otp.delete()  
#         return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)

# class VerifyOTPAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         email = request.data.get('email')
#         otp_code = request.data.get('otp_code')

#         if not email or not otp_code:
#             return Response({'error': 'Mobile number and OTP code are required'}, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user = User.objects.filter(email=email).first()
#             otp = OTP.objects.filter(user=user, otp_code=otp_code).latest('created_at')
#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
#         except OTP.DoesNotExist:
#             return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
#         otp.delete()  
#         return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)


class VerifyOTPAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        password = request.data.get('password')

        if not email or not otp_code or not password:
            return Response({'error': 'Email, OTP code, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        try:
            otp = OTP.objects.filter(user=user, otp_code=otp_code).latest('created_at')
        except OTP.DoesNotExist:
            return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class VerifyOTPAPIView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         mobile_no = request.data.get('mobile_no')
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        if otp.expiration_time > timezone.now():
            return Response({'error': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        authenticated_user = authenticate(request, username=email, password=password)
        if authenticated_user is None:
            return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
        otp.delete()
        return Response({f'{email}': f'{email} !! Login successful'}, status=status.HTTP_200_OK)


class BisunessApiview(APIView):
    def post(self,request):
        serializer = BusinessListingSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Msg":"The business listing is successfully created."},status=status.HTTP_201_CREATED)
        else:
            return Response({"Msg":"The request payload is missing required fields or contains invalid data."},status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk=None, format=None):
        if pk is not None:
            try:
                businessobj = BusinessListing.objects.get(id=pk)
                serializer = BusinessListingSerializer(businessobj)
                return Response({"msg": "Business details are successfully retrieved.", "data": serializer.data}, status=status.HTTP_200_OK)
            except BusinessListing.DoesNotExist:
                return Response({"msg": "No business exists with the given ID."}, status=status.HTTP_404_NOT_FOUND)
        location = request.GET.get('business_location')
        max_distance = request.GET.get('distance')
        queryset = BusinessListing.objects.all()
        if location:
            queryset = queryset.filter(business_location__icontains=location)
        if max_distance:
            try:
                max_distance = float(max_distance)
            except ValueError:
                return Response({"msg": "Distance must be a valid number."}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(distance__lte=max_distance)
        serializer = BusinessListingSerializer(queryset, many=True)
        return Response({"msg": "Businesses successfully retrieved.", "data": serializer.data}, status=status.HTTP_200_OK)
       
    def put(self,request,pk=None,format=None):
        try:
            id = pk 
            businessobj = BusinessListing.objects.get(id=pk) 
            serializer = BusinessListingSerializer(businessobj,data=request.data, partial=False) 
            if serializer.is_valid(raise_exception=True):
                return Response({"Msg":"The business listing is successfully updated."},status=status.HTTP_200_OK)
        except BusinessListing.DoesNotExist:
            return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self,request,pk,format=None):
        try:
            id = pk 
            businessobj = BusinessListing.objects.get(id=pk) 
            businessobj.delete()
            return Response({"Msg":"The business listing is successfully deleted."})
        except BusinessListing.DoesNotExist:
            return Response({"error": "Resource not found"}, status=status.HTTP_404_NOT_FOUND)


class ShopDetailView(APIView):
    def get(self,request,pk=None,format=None):
        try:
            id = pk 
            if id is not None:
                shop = ShopListing.objects.get(id=id)
                serializer = ShopSerializer(shop) 
                return Response({"serializes_data":serializer.data},status=status.HTTP_200_OK) 
            shop = ShopListing.objects.all()
            serializer = ShopSerializer(shop,many=True)
            return Response({"serializes_data":serializer.data},status=status.HTTP_200_OK) 
        except ShopListing.DoesNotExist:
            return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)
        

class Shopratingcomment(APIView):
    def post(self,request,format=None):
        try:
            serializer = RatcomSerializer(data=request.data) 
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Msg":serializer.data},status=status.HTTP_201_CREATED) 
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Shop not found'}, status=status.HTTP_404_NOT_FOUND)


class HaircutboyDetails(APIView):
    def post(self,request,format=None):
        try:
            serializer = HaircutSerializer(data=request.data) 
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Msg":serializer.data},status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST) 
        except Exception as e:
            return Response({'error': 'boys not found'}, status=status.HTTP_404_NOT_FOUND)

class Appointmentcustomerview(APIView):
    def post(self,request,format=None):
        try:
            serializer = AppointmentSerializer(data=request.data) 
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Msg":"Your visit to Barber's Haven is scheduled for 2024-08-20 at 3:00 PM."},status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'appointment customer not found'}, status=status.HTTP_404_NOT_FOUND)
        

class AdvertismentView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request,format=None):
        try:
            serializer = AdvertismentSerializer(data=request.data) 
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"Msg":serializer.data},status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_404_NOT_FOUND) 
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,pk=None,format=None):
        if pk is not None:
            try:
                advertismentobj = Advertisement.objects.get(id=pk) 
                serializer = AdvertismentSerializer(advertismentobj) 
                return Response({"msg":"Advertisment details are successfully retrieved ","data":serializer.data},status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"msg": "No advertise exists with the given ID."}, status=status.HTTP_404_NOT_FOUND)

        location = request.GET.get('location')
        age = request.GET.get('age')
        range = request.GET.get('range')

        advertisment = Advertisement.objects.all() 
        if location:
            advertisment = Advertisement.objects.filter(location__icontains=location)
        if age:
            advertisment = Advertisement.objects.filter(age__icontains=age)
        if range:
            advertisment = Advertisement.objects.filter(range__icontains=range)

        serializer = AdvertismentSerializer(advertisment,many=True)
        return Response({"Msg":"Advertsiment rettieved successfully","data":serializer.data},status=status.HTTP_200_OK)

    def delete(self,request,pk,format=None):
        try:
            id = pk 
            advertisment = Advertisement.objects.get(id=pk)
            advertisment.delete() 
            return Response({"Msg":"Advertisment has deleted successfully !"})
        except Advertisement.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class ForgotPasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
        send_mail(
            'Password Reset Request',
            f'Click the link below to reset your password:\n{reset_url}',
            'mk2648054@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
    
    
class PasswordResetConfirmView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            new_password = request.data.get('new_password')
            confirm_new_password = request.data.get('confirm_new_password')
            if not new_password or not confirm_new_password:
                return Response({'error': 'Both new password and confirm password are required'}, status=status.HTTP_400_BAD_REQUEST)
            if new_password != confirm_new_password:
                return Response({'error': 'New password and confirm password do not match'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



# class ChangePasswordView(APIView):
#      permission_classes = [permissions.AllowAny]
#      def post(self,request ,*args):
#         serializer = ChangePasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = User.objects.get(email=serializer.data.get('email'))
#         if not user.check_password(serializer.data.get('old_password')):
#                 return Response({'password': 'Invalid old password'}, status=400)
#         user.set_password(serializer.validated_data['new_password']) 
#         user.save()
#         return Response({'detail': 'Password changed successfully'})



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    def get_object(self, email):
        User = get_user_model()
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            email = serializer.validated_data['email']
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user = self.get_object(email)
            if not user:
                return Response({"email": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
            if not user.check_password(old_password):
                return Response({"old_password": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password has been changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
        serializer_class = LogoutSerializer 
        permission_classes = [permissions.AllowAny]	
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]

        def post(self, request,*args):
             serializer = self.serializer_class(data=request.data)
             serializer.is_valid(raise_exception=True)
             serializer.save() 
             return Response({'status':status.HTTP_204_NO_CONTENT,'logout':'logout successfully'}) 


# class LoginAPIView(APIView):                                        
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         if not email or not password:
#             return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             return Response({
#                 'message': 'Login successful'
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)

class DeleteUserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user:
            user.is_active = False
            user.deactivated_at = timezone.now()
            user.save()
            return Response({'message': 'User has been deactivated and will be stored in the database for at least 90 days.After 90 days user has been deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

class DeleteUserInstantlyAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(email=email).first()
        if user:
            user.delete()  
            return Response({'message': 'User has been permanently deleted from the database.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
class AllUserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None, format=None):
        try:
            if pk is not None:
                user = User.objects.get(id=pk)
                serializer = RegisterSerializer(user)
                data = serializer.data
                filtered_data = {
                    'name': data.get('name'),
                    'email': data.get('email'),
                    'mobile_no': data.get('mobile_no')
                }
                return Response({"User details": filtered_data}, status=status.HTTP_200_OK)
            users = User.objects.all()
            serializer = RegisterSerializer(users, many=True)
            filtered_data = [
                {
                    'name': user_data.get('name'),
                    'email': user_data.get('email'),
                    'mobile_no': user_data.get('mobile_no')
                } for user_data in serializer.data
            ]
            return Response({"All User": filtered_data}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)