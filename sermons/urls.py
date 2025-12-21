from django.urls import path
from . import views

urlpatterns = [
    path('', views.SermonListView.as_view(), name='sermon_list'),
    path('<slug:slug>/', views.SermonDetailView.as_view(), name='sermon_detail'),
]
