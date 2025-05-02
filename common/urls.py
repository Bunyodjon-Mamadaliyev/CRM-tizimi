from django.urls import path
from .views import (
    SalesReportView, ActivitiesReportView,
    CompaniesReportView, DealsReportView
)

urlpatterns = [
    path('reports/sales/', SalesReportView.as_view(), name='sales-report'),
    path('reports/activities/', ActivitiesReportView.as_view(), name='activities-report'),
    path('reports/companies/', CompaniesReportView.as_view(), name='companies-report'),
    path('reports/deals/', DealsReportView.as_view(), name='deals-report'),
]
