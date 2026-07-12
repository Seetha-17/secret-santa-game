import csv
import os
from typing import List, Dict
from models.employee import Employee
from models.assignment import SecretSantaAssignment

class CSVHandler:
    @staticmethod
    def read_employees_list(file_path: str) -> List[Employee]:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Missing file: {file_path}")
        
        employees = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                employees.append(Employee(row['Employee_Name'].strip(), row['Employee_EmailID'].strip()))
        return employees

    @staticmethod
    def read_historical_map(file_path: str) -> Dict[Employee, Employee]:
        if not file_path or not os.path.exists(file_path):
            return {}
        
        history_map = {}
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                giver = Employee(row['Employee_Name'].strip(), row['Employee_EmailID'].strip())
                child = Employee(row['Secret_Child_Name'].strip(), row['Secret_Child_EmailID'].strip())
                history_map[giver] = child
        return history_map

    @staticmethod
    def write_assignments_out(file_path: str, assignments: list) -> None:
        with open(file_path, mode='w', encoding='utf-8', newline='') as f:
            fields = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for item in assignments:
                writer.writerow({
                    'Employee_Name': item.employee.name,
                    'Employee_EmailID': item.employee.email,
                    'Secret_Child_Name': item.secret_child.name,
                    'Secret_Child_EmailID': item.secret_child.email
                })