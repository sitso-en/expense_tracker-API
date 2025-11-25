from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('expenses', views.ExpenseViewSet, basename='expenses')
router.register('categories', views.CategoryViewSet)


urlpatterns = [
    path('monthlysummary/', views.MonthlySummaryView.as_view(), name='monthly_summary'),
    path('yearlysummary/', views.YearlySummaryView.as_view(), name='yearly-summary'),
    path('log/', views.log, name='log'),
]+ router.urls