from django.urls import path
from user import views




urlpatterns = [
    path("signup/", views.UserSignUpView.as_view(),),
    path("registers/", views.UsersListView.as_view(),), #por tupla va  la coma
    path("email-verify/", views.VerifyEmail.as_view(), name='email-verify',),
    path("login/", views.LoginAPIViews.as_view(), name='login',),
    path('request-reset-email/', views.RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')    
]