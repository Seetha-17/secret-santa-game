class Employee:
    def _init_(self, name: str, email: str):
        self.name = name
        self.email = email

    # This helps Python compare employees correctly when eliminating last year's children
    def _eq_(self, other):
        if not isinstance(other, Employee):
            return False
        return self.email == other.email

    def _hash_(self):
        return hash(self.email)