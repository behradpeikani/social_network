from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.posts_list, name='posts_list'),
    path('detail/<str:post_id>/', views.post_detail, name='post_detail'),
    path('add_post/<int:user_id>/', views.add_post, name='add_post'),
    path('delete_post/<int:user_id>/<str:post_id>/', views.delete_post, name='delete_post'),
    path('edit_post/<int:user_id>/<str:post_id>/', views.edit_post, name='edit_post'),
    path('add_reply/<str:post_id>/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('like/<str:post_id>/', views.like_view, name='like_view'),
    path('unlike/<str:post_id>/', views.unlike_view, name='unlike_view'),
]