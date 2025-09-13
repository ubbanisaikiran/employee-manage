from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .mongo_client import employees_collection
from .serializers import EmployeeSerializer
from django.shortcuts import render
from datetime import datetime

# Home page
def home(request):
    return render(request, 'home.html')

# List Employees
@api_view(['GET'])
def list_employees(request):
    employees = list(employees_collection.find({}, {"_id": 0}))
    return Response(employees)

# Create Employee (separate)
@api_view(['POST'])
def create_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data

        # Convert joining_date to ISO string
        if "joining_date" in data and hasattr(data["joining_date"], "isoformat"):
            data["joining_date"] = data["joining_date"].isoformat()

        # Check uniqueness
        if employees_collection.find_one({"employee_id": data["employee_id"]}):
            return Response({"error": "Employee ID must be unique"}, status=status.HTTP_400_BAD_REQUEST)

        employees_collection.insert_one(data)
        saved_employee = employees_collection.find_one({"employee_id": data["employee_id"]}, {"_id": 0})
        return Response(saved_employee, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Employee Detail (GET, PUT, DELETE)
@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, employee_id):
    if request.method == 'GET':
        employee = employees_collection.find_one({"employee_id": employee_id}, {"_id": 0})
        if not employee:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(employee)

    if request.method == 'PUT':
        update_data = {k: v for k, v in request.data.items()}
        result = employees_collection.update_one({"employee_id": employee_id}, {"$set": update_data})
        if result.matched_count == 0:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        employee = employees_collection.find_one({"employee_id": employee_id}, {"_id": 0})
        return Response(employee)

    if request.method == 'DELETE':
        result = employees_collection.delete_one({"employee_id": employee_id})
        if result.deleted_count == 0:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Employee deleted successfully"})
# Average Salary by Department
@api_view(['GET'])
def avg_salary_by_department(request):
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}}
    ]
    result = list(employees_collection.aggregate(pipeline))
    formatted = [{"department": r["_id"], "avg_salary": r["avg_salary"]} for r in result]
    return Response(formatted)

@api_view(['GET'])
def search_employees_by_skill(request):
    skill = request.query_params.get('skill', None)
    if not skill:
        return Response({"error": "Skill parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    # Find employees whose skills array contains the specified skill
    employees = list(employees_collection.find(
        {"skills": {"$in": [skill]}},
        {"_id": 0}
    ))

    return Response(employees)

@api_view(['GET'])
def list_employees_by_department(request):
    department = request.query_params.get('department')
    if not department:
        return Response(
            {"error": "Department parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    employees = list(
        employees_collection.find(
            {"department": department},
            {"_id": 0}
        ).sort("joining_date", -1)
    )

    return Response(employees)
