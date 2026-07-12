from models.employee import Employee

class Assignment:  # <--- Make sure this matches exactly
    def _init_(self, employee: Employee, secret_child: Employee):
        self.employee = employee
        self.secret_child = secret_child
