from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from foodrec import views

urlpatterns = [
    path('food/', views.FoodList.as_view()),
    path('food/<int:pk>/', views.FoodDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)