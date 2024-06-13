from django.urls import path
from . import views
urlpatterns = [
    path('<str:username>/', views.home, name='home'),
    path('<str:username>/delete-profile/', views.delete_profile, name='delete_profile'),
    path('<str:username>/log-out/', views.log_out, name='log_out'),
    path('<str:username>/edit-profile/', views.edit_profile, name='edit_profile'),
    path('<str:username>/change-username/', views.change_username, name='change_username'),
    path('<str:username>/change-email/', views.change_email, name='change_email'),
    path('<str:username>/change-password/', views.change_password, name='change_password'),
    path('<str:username>/add-course/', views.add_course, name='add-course'),
    path('<str:username>/<str:coursename>/', views.view_course, name='view_course'),
    path('<str:username>/<str:coursename>/delete-course/', views.delete_course, name='delete_course'),
    path('<str:username>/<str:coursename>/add-class/', views.add_class, name='add_class'),
    path('<str:username>/<str:coursename>/<str:classname>/', views.view_class, name='view_class'),
    path('<str:username>/<str:coursename>/<str:classname>/delete-class/', views.delete_class, name='delete_class'),
    path('<str:username>/<str:coursename>/<str:classname>/add-event/', views.add_event, name='add_event'),
    path('<str:username>/<str:coursename>/<str:classname>/<int:event_id>/delete-event/', views.delete_event, name='delete_event'),
    path('<str:username>/<str:coursename>/<str:classname>/<int:event_id>/checkin/', views.check_in, name='check_in'),
        
]