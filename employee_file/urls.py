from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # CRUD
    path('employees/', views.list_employees, name='list_employees'),   # GET (list only)
    path('employees/create/', views.create_employee, name='create_employee'), # POST (create via form/API)
    path('employees/<str:employee_id>/', views.employee_detail, name='employee_detail'), # GET/PUT/DELETE

 # Queries (support with or without / at end)
    re_path(r'^employees/avg-salary?$', views.avg_salary_by_department, name='avg_salary_by_department'),
    re_path(r'^employees/search?$', views.search_employees_by_skill, name='search_by_skill'),
    re_path(r'^employees/department/?$', views.list_employees_by_department, name='list_employees_by_department'),
]
