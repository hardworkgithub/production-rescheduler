from django.urls import path
from . import views

urlpatterns = [
    path('reschedule/', views.api_reschedule),  # React calls: /api/reschedule/
]