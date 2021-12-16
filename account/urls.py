from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
	path('register/', views.register_view, name='register_view'),
    path('profile/<int:pk>/', views.dashboard_view, name='dashboard_view'),
    path('edit_profile/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('all_profiles/', views.all_profiles, name='all_profiles'),
    path('profile/<int:pk>/follow/', views.AddFollower.as_view(), name='follow'),
    path('profile/<int:pk>/unfollow/', views.RemoveFollower.as_view(), name='unfollow'),
    path('profile/<int:pk>/followers_list/', views.FollowersList.as_view(), name='followers_list')
]