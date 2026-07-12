from .employee import Employee

class SecretSantaAssignment:
    def __init__(self, employee: Employee, secret_child: Employee):
        self.employee = employee
        self.secret_child = secret_child