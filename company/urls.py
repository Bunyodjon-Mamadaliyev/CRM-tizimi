from django.urls import path
from .views import (
    CompanyListCreateView,
    CompanyRetrieveUpdateDestroyView,
    CompanyContactsView,
    CompanyDealsView,
    CompanyActivitiesView
)

urlpatterns = [
    path('companies/', CompanyListCreateView.as_view(), name='company-list-create'),
    path('companies/<int:pk>/', CompanyRetrieveUpdateDestroyView.as_view(), name='company-retrieve-update-destroy'),
    path('companies/<int:pk>/contacts/', CompanyContactsView.as_view(), name='company-contacts'),
    path('companies/<int:pk>/deals/', CompanyDealsView.as_view(), name='company-deals'),
    path('companies/<int:pk>/activities/', CompanyActivitiesView.as_view(), name='company-activities'),
]