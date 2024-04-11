from django.urls import path

from user import views

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user-register"),
    path("login/", views.UserLoginView.as_view(), name="user-login"),

]
