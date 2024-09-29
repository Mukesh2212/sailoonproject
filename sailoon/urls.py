
from django.contrib import admin
from django.urls import path
from sailoonapp import views 
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.UserRegistrationView.as_view(), name='user-registration'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('verify-otp/', views.VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('business-details/',views.BisunessApiview.as_view(),name="bisunessdetails"),
    path('business-details/<int:pk>/',views.BisunessApiview.as_view(),name="bisunessdetails"),
    path('shopdetails/<int:pk>/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('shopdetails/', views.ShopDetailView.as_view(), name='shop-detail'),
    path('rate/', views.Shopratingcomment.as_view(), name='rate-detail'),
    path('visit/', views.HaircutboyDetails.as_view(), name='haircutboy-detail'),
    path('appoinmentcut/', views.Appointmentcustomerview.as_view(), name='appoinmentcut'),
    path('advertisment/', views.AdvertismentView.as_view(), name='appoinmentcust'),
    path('advertisment/<int:pk>/', views.AdvertismentView.as_view(), name='appoinmentcust'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password'),
    path('api/reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-passwords'),
    path("logout/",views.LogoutView.as_view(), name="logout_view"),
    path('delete/',views.DeleteUserAPIView.as_view(),name='delete-user'),
    path('delete-instant/',views.DeleteUserInstantlyAPIView.as_view(),name='delete-user'),
    path('alluser/',views.AllUserView.as_view(),name='all-user'),
    path('alluser/<int:pk>/',views.AllUserView.as_view(),name='all-user'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
