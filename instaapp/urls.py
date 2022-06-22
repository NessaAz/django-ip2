from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index' ),
    path('signup/',views.signup, name='signup' ),
    path('login/',views.loginuser, name='loginuser' ),
    path('logout/', views.loginuser, name='loginuser'),
   	path('newpost/', views.newpost, name='newpost'),
    path('<uuid:post_id>', views.postdetail, name='postdetail'),
    path('notifications/', views.shownotifications, name='show-notifications'),
   	path('<noti_id>/delete', views.deletenotification, name='delete-notification'),
    path('<username>/', views.profileuser, name='profileuser'),
    path('<username>/saved', views.profilefavorite, name='profilefavorite'),
    path('tag/<slug:tag_slug>', views.tag, name='tag'),
    path('<uuid:post_id>/like', views.postlike, name='postlike'),
   	path('<uuid:post_id>/favorite', views.favorite, name='favorite'),
    path('searchuser/', views.searchuser, name='searchuser'),
]
