from django.urls import path
from . import views


urlpatterns = [
    path('user/create/', views.CreateUserApiView.as_view(), name='create_user')
]