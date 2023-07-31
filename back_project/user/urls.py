from django.urls import path
from user import views

urlpatterns = [
    path("signup/", views.UserSignUpView.as_view(),),
    path("registers/", views.UsersListView.as_view(),), #por tupla va  la coma
]