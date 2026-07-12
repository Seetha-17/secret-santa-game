class Employee:
    def _init_(self, name: str, email: str):
        self.name = name.strip()
        self.email = email.strip().lower()

    def _eq_(self, other):
        return isinstance(other, Employee) and self.email == other.email

    def _hash_(self):
        return hash(self.email)