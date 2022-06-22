from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index' ),
    path('signup/',views.signup, name='signup' ),
    path('login/',views.loginuser, name='loginuser' ),
   	path('newpost/', views.newpost, name='newpost'),
    path('<uuid:post_id>', views.postdetail, name='postdetail'),
    path('notifications/', views.shownotifications, name='show-notifications'),
   	path('<noti_id>/delete', views.deletenotification, name='delete-notification'),
]
