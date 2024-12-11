from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, EmployeeSerializer
from .models import Employee

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
