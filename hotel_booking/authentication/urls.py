from django.urls import path
from . import views
from .views import *

urlpatterns = [
    # path('', views.HiAuthView.as_view(), name='hi_auth'),
    path('signup/', views.RegistrationView.as_view(), name='sign_up'),
    path('activate/', ActivationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('forgot_password/', ForgotPasswordView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompleteView.as_view()),

]