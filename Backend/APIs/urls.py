from django.urls import path
from .views import EmployeeRegistrationView
from .views import CompanyListCreateView, CompanySingleView



urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name="create_new_employee"),
    path('company/', CompanyListCreateView.as_view(), name="create_list_company"),
    path('company/<int:pk>/', CompanySingleView.as_view(), name="company_details"),
]