import unittest
from models.employee import Employee
from services.matcher import SecretSantaMatcher

class TestSecretSantaMatcher(unittest.TestCase):
    def setUp(self):
        self.e1 = Employee("Alice", "alice@acme.com")
        self.e2 = Employee("Bob", "bob@acme.com")
        self.e3 = Employee("Charlie", "charlie@acme.com")
        self.employees = [self.e1, self.e2, self.e3]

    def test_no_self_assignment_and_completeness(self):
        matcher = SecretSantaMatcher(self.employees, {})
        assignments = matcher.generate_assignments()
        
        self.assertEqual(len(assignments), 3)
        for a in assignments:
            self.assertNotEqual(a.employee.email, a.secret_child.email)

    def test_honors_previous_year_constraints(self):
        history = {"alice@acme.com": "bob@acme.com"}
        matcher = SecretSantaMatcher(self.employees, history)
        assignments = matcher.generate_assignments()
        
        for a in assignments:
            if a.employee.email == "alice@acme.com":
                self.assertNotEqual(a.secret_child.email, "bob@acme.com")

if __name__ == '__main__':
    unittest.main()