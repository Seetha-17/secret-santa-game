import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse # Added HTMLResponse
from models.employee import Employee
from services.csv_handler import CSVHandler
from services.matcher import SecretSantaMatcher

app = FastAPI()

EMPLOYEE_FILE = "employees.csv"
PREVIOUS_ASSIGNMENTS_FILE = "previous_year_assignments.csv"
OUTPUT_FILE = "current_assignments.csv"

# ==========================================
# NEW BASE ROUTE TO SERVE THE HTML WEB INTERFACE
# ==========================================
@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    """
    Serves the front-end dashboard directly when loading the root URL.
    """
    template_path = os.path.join("templates", "index.html")
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="HTML template file structure missing on server instance.")
        
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

# Your existing POST generation route
@app.post("/generate-assignments/")
def generate_assignments(payload: dict):
    try:
        if not os.path.exists(EMPLOYEE_FILE):
            return {"status": "error", "detail": f"Missing input file: {EMPLOYEE_FILE}"}
            
        # 1. CHANGE THIS LINE from read_employees to read_employees_list
        employees = CSVHandler.read_employees_list(EMPLOYEE_FILE)
        
        previous_assignments = {}
        if os.path.exists(PREVIOUS_ASSIGNMENTS_FILE):
            # 2. CHANGE THIS LINE from read_previous_assignments to read_historical_map
            previous_assignments = CSVHandler.read_historical_map(PREVIOUS_ASSIGNMENTS_FILE)
        
        matcher = SecretSantaMatcher(employees, previous_assignments)
        assignments = matcher.assign()
        
        # 3. CHANGE THIS LINE to match your exact export function name (write_assignments_out)
        CSVHandler.write_assignments_out(OUTPUT_FILE, assignments)
        return {"status": "success", "message": "Assignments successfully generated!"}
        
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Your existing GET download route
@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    # Check if running as a compiled standalone executable bundle
    base_path = getattr(sys, 'MEIPASS', os.path.dirname(os.path.abspath(file_)))
    template_path = os.path.join(base_path, "templates", "index.html")
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="HTML template file structure missing on instance.")
        
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "_main_":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)