import random
from typing import List, Dict
from models.employee import Employee
from models.assignment import SecretSantaAssignment

class SecretSantaMatcher:
    def _init_(self, employees: List[Employee], previous_assignments: Dict[Employee, Employee] = None):
        """
        Constructor to initialize the participants list and previous pairings history.
        """
        self.employees = employees
        self.previous_assignments = previous_assignments or {}

    def assign(self, max_attempts: int = 2000) -> List[SecretSantaAssignment]:
        """
        Calculates valid randomized Secret Santa assignments matching all constraints.
        """
        if len(self.employees) < 2:
            raise ValueError("At least 2 employees are required to run Secret Santa.")

        for _ in range(max_attempts):
            pool = self.employees.copy()
            random.shuffle(pool)
            
            if self._is_valid_shuffle(self.employees, pool):
                return [SecretSantaAssignment(emp, child) for emp, child in zip(self.employees, pool)]
                
        raise ValueError("Could not find a valid assignment configuration matching all constraints after maximum retries.")

    def _is_valid_shuffle(self, givers: List[Employee], receivers: List[Employee]) -> bool:
        for giver, receiver in zip(givers, receivers):
            # Constraint 1: Cannot match an employee with themselves
            if giver == receiver:
                return False
            # Constraint 2: Cannot match with the same secret child as last year
            if self.previous_assignments.get(giver) == receiver:
                return False
        return True