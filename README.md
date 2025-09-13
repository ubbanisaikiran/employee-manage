

## Overview

This is a Django REST Framework project for managing employees. It supports creating, reading, updating, deleting employees, listing by department, computing average salary by department, and searching by skill. MongoDB is used as the database.

---

## Prerequisites

* Python 3.11+
* MongoDB running locally or remotely
* pip (Python package manager)

---

## Installation & Setup

1. **Clone or extract the project**:

   ```bash
   unzip employee_project.zip
   cd employee_project
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/Scripts/activate       # Windows: venv\Scripts\activate
   ```

3. **Configure MongoDB**:
   Update `mongo_client.py` with your MongoDB connection string:

   ```python
   from pymongo import MongoClient
   client = MongoClient("mongodb://localhost:27017/")
   db = client['employee_db']
   employees_collection = db['employees']
   ```

4. **Run the server**:

   ```bash
   python manage.py runserver
   ```


Do you want me to do that next?
