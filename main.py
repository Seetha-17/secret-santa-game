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
            
        employees = CSVHandler.read_employees(EMPLOYEE_FILE)
        
        previous_assignments = {}
        if os.path.exists(PREVIOUS_ASSIGNMENTS_FILE):
            previous_assignments = CSVHandler.read_previous_assignments(PREVIOUS_ASSIGNMENTS_FILE)
        
        matcher = SecretSantaMatcher(employees, previous_assignments)
        assignments = matcher.assign()
        
        CSVHandler.write_assignments(OUTPUT_FILE, assignments)
        return {"status": "success", "message": "Assignments successfully generated!"}
        
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Your existing GET download route
@app.get("/download-assignments/")
def download_assignments():
    if not os.path.exists(OUTPUT_FILE):
        raise HTTPException(status_code=404, detail="Assignments file not found. Generate first.")
    return FileResponse(path=OUTPUT_FILE, media_type="text/csv", filename="secret_santa_assignments.csv")

if __name__ == "_main_":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)