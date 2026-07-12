import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from models.employee import Employee
from services.csv_handler import CSVHandler
from services.matcher import SecretSantaMatcher

# 1. Initialize the FastAPI app object
app = FastAPI()

# Configuration for paths
EMPLOYEE_FILE = "employees.csv"
PREVIOUS_ASSIGNMENTS_FILE = "previous_year_assignments.csv"
OUTPUT_FILE = "current_assignments.csv"

@app.post("/generate-assignments/")
def generate_assignments(payload: dict):
    """
    This endpoint parses employee files, applies business logic rules, 
    and generates the current year's Secret Santa assignments.
    """
    try:
        # Step 1: Check if input files exist on the server
        if not os.path.exists(EMPLOYEE_FILE):
            return {"status": "error", "detail": f"Missing input file: {EMPLOYEE_FILE}"}
            
        # Step 2: Read employees and historical data using your handler modules
        employees = CSVHandler.read_employees(EMPLOYEE_FILE)
        
        # Load previous history if it exists, otherwise pass an empty dictionary
        previous_assignments = {}
        if os.path.exists(PREVIOUS_ASSIGNMENTS_FILE):
            previous_assignments = CSVHandler.read_previous_assignments(PREVIOUS_ASSIGNMENTS_FILE)
        
        # Step 3: Run the core matching rules engine
        matcher = SecretSantaMatcher(employees, previous_assignments)
        assignments = matcher.assign()
        
        # Step 4: Save output to disk
        CSVHandler.write_assignments(OUTPUT_FILE, assignments)
        
        return {"status": "success", "message": "Assignments successfully generated!"}
        
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/download-assignments/")
def download_assignments():
    """
    This endpoint downloads the generated Secret Santa assignments CSV file directly.
    """
    # Verify the output file has actually been generated on disk first
    if not os.path.exists(OUTPUT_FILE):
        raise HTTPException(
            status_code=404, 
            detail="Assignments file not found. Please run the generation endpoint first."
        )
    
    # Safely stream the file directly to the user's browser download bar
    return FileResponse(
        path=OUTPUT_FILE, 
        media_type="text/csv", 
        filename="secret_santa_assignments.csv"
    )

# Keep your local testing block at the bottom
if __name__ == "_main_":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)