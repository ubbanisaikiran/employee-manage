from djongo import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    salary = models.FloatField()
    joining_date = models.DateField()
    skills = models.JSONField()   # store as array

    def __str__(self):
        return f"{self.employee_id} - {self.name}"
