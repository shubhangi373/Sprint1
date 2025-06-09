from django.urls import path
from . import views
path('', views.home, name='home'),
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('update/<int:complaint_id>/', views.update_status, name='update_status'),
    path('', views.submit_complaint, name='submit_complaint'),
]
