from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path("", views.account_sitaram, name="sitaram"),
    path("activate/<int:msid>/<int:mobile>", views.account_activate, name="account_activate"),
    path("login/", views.account_login, name="account_login"),
    path("logout/", views.account_logout, name="account_logout"),
    path("register/", views.account_register, name="account_register"),
    path("features/", views.sitaram_features, name="sitaram_features"),
    path("password/", views.account_password, name="account_password"),
]