from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, EmployeeSerializer
from .serializers import CompanySerializer, DepartmentSerializer
from .models import Employee, Company, Department
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest
from rest_framework.decorators import api_view
from django.contrib.sessions.models import Session
from rest_framework.permissions import IsAuthenticated

class EmployeeRegistrationView(APIView):
    def post(self, request):
        # Extract data related to the user from the request
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        password_confirmation = request.data.get("password_confirmation")
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "password_confirmation": password_confirmation,
        }

        # Validate the extracted data using the custom User serializer created then save the user
        user_serializer = UserRegistrationSerializer(data=user_data)
        if user_serializer.is_valid():
            user = user_serializer.save()

            # Extract employee-specific data
            first_name = request.data.get("first_name")
            last_name = request.data.get("last_name")
            phone_number = request.data.get("phone_number")
            address = request.data.get("address")
            company_id = request.data.get("company")
            department_id = request.data.get("department")
            date_hired = request.data.get("date_hired")
            salary = request.data.get("salary")

            # Prepare data for the Employee model
            employee_data = {
                "first_name": first_name,
                "last_name": last_name,
                "user": user.id,
                "phone_number": phone_number,
                "address": address,
                "company": company_id,
                "department": department_id,
                "date_hired": date_hired,
                "salary": salary,
            }

            # Validate and save the employee
            employee_serializer = EmployeeSerializer(data=employee_data)
            if employee_serializer.is_valid():
                employee_serializer.save()
                return Response({"message": "Employee registered successfully"}, status=status.HTTP_201_CREATED)
            else:
                # Delete the user if employee data is invalid
                user.delete()
                return Response(employee_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyListCreateView(APIView):

    permission_classes = [IsAuthenticated]
    # retreive all records of the Company table from database
    def get(self, request):
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    #creates a new Company and stores it in the database
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanySingleView(APIView):

    permission_classes = [IsAuthenticated]
    # handle GET calls for a single Company object to retrieve it
    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    # handle PUT call to udpate any company instance
    def put(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # handles deleting a company from the database with a certain primary key
    def delete(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DepartmentListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartmentSingleView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    def put(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def employee_login_view(request: HttpRequest):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request=request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Get additional employee data
            try:
                employee = Employee.objects.get(user=user)
                employee_data = {
                    "id": user.id,
                    "username": user.username,
                    "first_name": employee.first_name,
                    "last_name": employee.last_name,
                    "email": user.email,
                    "phone_number": employee.phone_number,
                    "address": employee.address,
                    "company": employee.company.name,
                    "department": employee.department.name,
                    "date_hired": employee.date_hired,
                    "salary": str(employee.salary),  # Convert Decimal to string for JSON serialization
                }
                return Response(employee_data)
            except Employee.DoesNotExist:
                return Response(
                    {"message": "Employee profile does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"message": "Username or password is incorrect"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

@api_view(["POST"])
def logout_view(request: HttpRequest):
    logout(request)
    Session.objects.filter(session_key=request.session.session_key).delete()

    return Response({"message": "successfully loged out !!!"})