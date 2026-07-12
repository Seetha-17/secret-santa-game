from models.employee import Employee

<<<<<<< HEAD
class SecretSantaAssignment:
    def __init__(self, employee: Employee, secret_child: Employee):
=======
class Assignment:  # <--- Make sure this matches exactly
    def _init_(self, employee: Employee, secret_child: Employee):
>>>>>>> a53b3a2 (fix:corrected class name import mismatch for assignments)
        self.employee = employee
        self.secret_child = secret_child
