from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_user, name='login'),
    path('register/', views.register_user, name='register'),
    path('logout/', views.logout_user, name='logout'),
    path('sellerhome/', views.sellerhome, name='sellerhome'),
    path('addland/', views.add_land, name='addland'),
    path('viewland/',views.view_land, name='viewland'),
    path('makerequest/<int:id>',views.request_land, name='makerequst'),
    path('viewrequest/',views.view_land_requests, name='viewrequest'),
    path('updaterequest/<int:id>',views.update_request, name='updaterequest'),
    path('seller_lands/',views.seller_lands, name='seller_lands'),
    path('buyer_landrequests/',views.buyer_landrequest, name='buyer_landrequest'),
    path('add_registration/',views.add_registration, name='add_registration'),
    path('delete_land/<int:id>',views.delete_land, name='delete_land'),
    path('register_land/<int:id>',views.register_land, name='register_land'),
    path('buyer_registrations/',views.buyer_registrations, name='buyer_registration'),
]