from django.urls import path

from . import views


app_name = 'website'

urlpatterns = [
	path('', views.HomepageView.as_view(), name='homepage'),
    path("login/", views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
	path('team/<int:pk>/', views.TeamDetailView.as_view(), name='team_detail'),
    path('team/create/', views.TeamCreate.as_view(), name='team_create'),
    path('team/update/<int:pk>/', views.TeamUpdate.as_view(), name='team_update'),
    path('team/delete/<int:pk>/', views.TeamDelete.as_view(), name='team_delete'),
]