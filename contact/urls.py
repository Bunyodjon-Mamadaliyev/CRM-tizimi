from django.urls import path
from .views import ContactListCreateView, ContactRetrieveUpdateDestroyView

urlpatterns = [
    path('contacts/', ContactListCreateView.as_view(), name='contact-list'),
    path('contacts/<int:id>/', ContactRetrieveUpdateDestroyView.as_view(), name='contact-detail'),
]