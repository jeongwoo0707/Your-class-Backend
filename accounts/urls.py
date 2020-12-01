from django.urls import path

from . import views

app_name = "user"
urlpatterns = [
    path('register', views.UserRegisterApiView.as_view(), name='register'),
    path('login', views.CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh', views.CustomTokenRefreshView.as_view(), name='refresh'),
    path('activate/<str:uidb64>/<str:token>', views.UserActivateApiView.as_view(), name='activate'),

    path('me/', views.ProfileManageApiView.as_view(), name='profile'),
    path('me/edit', views.UserManageApiView.as_view(), name='user-info-edit'),
    path('me/avatar', views.AvatarManageApiView.as_view(), name='avatar-edit'),
]