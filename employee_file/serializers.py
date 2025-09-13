from rest_framework import serializers

class EmployeeSerializer(serializers.Serializer):
    employee_id = serializers.CharField(max_length=20)
    name = serializers.CharField(max_length=100)
    department = serializers.CharField(max_length=50)
    salary = serializers.FloatField()
    joining_date = serializers.DateField()
    skills = serializers.ListField(child=serializers.CharField(max_length=50))
