from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from . import views

urlpatterns = [
    path("login", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("signup", views.SignUpView.as_view(), name="signup"),
    path("logout", views.LogoutView.as_view(), name="logout"),
]
