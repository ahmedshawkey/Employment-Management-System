from django.urls import path
from .views import EmployeeRegistrationView
from .views import CompanyListCreateView, CompanySingleView
from .views import DepartmentListCreateView, DepartmentSingleView
from .views import employee_login_view, logout_view


urlpatterns = [
    path('register/', EmployeeRegistrationView.as_view(), name="create_new_employee"),
    path('company/', CompanyListCreateView.as_view(), name="create_list_company"),
    path('company/<int:pk>/', CompanySingleView.as_view(), name="company_details"),
    path('department/', DepartmentListCreateView.as_view(), name="list_create_department"),
    path('department/<int:pk>/', DepartmentSingleView.as_view(), name="department_details"),
    path('login/', employee_login_view, name="employee_login_view"),
    path('logout/', logout_view, name="logout_view"),
]