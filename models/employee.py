class Employee:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    # This helps Python compare employees correctly when eliminating last year's children
    def __eq__(self, other):
        if not isinstance(other, Employee):
            return False
        return self.email == other.email

    def __hash__(self):
        return hash(self.email)