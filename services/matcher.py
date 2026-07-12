import random
from typing import List, Dict
from models.employee import Employee
from models.assignment import SecretSantaAssignment

class SecretSantaMatcher:
    def _init_(self, employees: List[Employee], history: Dict[str, str]):
        self.employees = employees
        self.history = history

    def generate_assignments(self) -> List[SecretSantaAssignment]:
        if len(self.employees) < 2:
            raise ValueError("Need at least 2 employees to play.")
        
        for attempt in range(1000):
            pool = self.employees.copy()
            random.shuffle(pool)
            assignments = []
            possible = True
            
            for giver in self.employees:
                valid_candidates = [
                    child for child in pool 
                    if child.email != giver.email and self.history.get(giver.email) != child.email
                ]
                
                if not valid_candidates:
                    possible = False
                    break
                
                chosen_child = random.choice(valid_candidates)
                pool.remove(chosen_child)
                assignments.append(SecretSantaAssignment(giver, chosen_child))
                
            if possible:
                return assignments
                
        raise RuntimeError("No valid Secret Santa configurations meet the historical constraints.")