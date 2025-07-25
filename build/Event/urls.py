from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),

    #homepage for CONGREGATE MEMBER
    path('homecon/', views.homecon_view, name='homecon'),
    path('homecon/eventBooking/', views.eventBooking, name='eventBooking'),
    path('homecon/event-schedule1/', views.event_schedule1_view, name='event_schedule1'),

    #homepage for MOSQUE COMMUNITY
    path('homemos/', views.homemos_view, name='homemos'),
    path('homemos/congregate-list/', views.congregate_list_view, name='congregate_list'),
    path('homemos/event-schedule2/', views.event_schedule2_view, name='event_schedule2'),
    path('homemos/event-schedule2/update/<int:event_id>/', views.event_update_view, name='event_update'),
    path('homemos/event-schedule2/delete/<int:event_id>/', views.event_delete_view, name='event_delete'),
    path('homemos/payment2/', views.payment2_view, name='payment2'),


    #homepage for HEAD OF MOSQUE COMMUNITY
    path('homehead/', views.homehead_view, name='homehead'),
    path('homehead/event_schedule', views.event_schedule, name='event_schedule'),
]
