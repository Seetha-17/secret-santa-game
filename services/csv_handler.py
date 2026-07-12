import csv
from typing import List, Dict
from models.employee import Employee
from models.assignment import SecretSantaAssignment

class CSVHandler:
    @staticmethod
    def load_employees(file_path: str) -> List[Employee]:
        employees = []
        with open(file_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                employees.append(Employee(row['Employee_Name'], row['Employee_EmailID']))
        return employees

    @staticmethod
    def load_history(file_path: str) -> Dict[str, str]:
        history = {}
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    history[row['Employee_EmailID'].strip().lower()] = row['Secret_Child_EmailID'].strip().lower()
        except FileNotFoundError:
            pass
        return history

    @staticmethod
    def save_assignments(file_path: str, assignments: List[SecretSantaAssignment]):
        fieldnames = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for a in assignments:
                writer.writerow({
                    'Employee_Name': a.employee.name,
                    'Employee_EmailID': a.employee.email,
                    'Secret_Child_Name': a.secret_child.name,
                    'Secret_Child_EmailID': a.secret_child.email
                })