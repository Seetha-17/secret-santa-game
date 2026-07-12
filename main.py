import sys
from services.csv_handler import CSVHandler
from services.matcher import SecretSantaMatcher

def main():
    try:
        print("Loading employee registries...")
        employees = CSVHandler.load_employees('employees.csv')
        history = CSVHandler.load_history('previous_assignments.csv')
        
        print("Running Secret Santa generation algorithms...")
        matcher = SecretSantaMatcher(employees, history)
        results = matcher.generate_assignments()
        
        print("Writing final assignments to CSV...")
        CSVHandler.save_assignments('secret_santa_output.csv', results)
        print("Successfully generated secret_santa_output.csv!")
        
    except Exception as e:
        print(f"Operational Execution Error: {e}", file=sys.stderr)

if __name__ == '_main_':
    main()