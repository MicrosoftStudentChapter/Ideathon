from django.urls import path
from . import views


app_name = 'website'

urlpatterns = [
	path('', views.HomepageView.as_view(), name='homepage'),
	path('collection/<int:pk>/', views.TeamDetailView.as_view(), name='collection_detail'),
    path('collection/create/', views.TeamCreate.as_view(), name='collection_create'),
    path('collection/update/<int:pk>/', views.TeamUpdate.as_view(), name='collection_update'),
]