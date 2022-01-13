from django.urls import path
from . import views

urlpatterns = [
    # path('', views.HiBookingsView.as_view(), name='hi_bookings'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list),
    path('api/messages/', views.message_list),
    path('api/users/', views.user_list),
]
