import sys
import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse # Added HTMLResponse
from models.employee import Employee
from services.csv_handler import CSVHandler
from services.matcher import SecretSantaMatcher

app = FastAPI()

# Automatically detects if running as an EXE to get the real directory path
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

EMPLOYEE_FILE = os.path.join(BASE_DIR, "employees.csv")
PREVIOUS_ASSIGNMENTS_FILE = os.path.join(BASE_DIR, "previous_year_assignments.csv")
OUTPUT_FILE = os.path.join(BASE_DIR, "current_assignments.csv")

# ==========================================
# NEW BASE ROUTE TO SERVE THE HTML WEB INTERFACE
# ==========================================
@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    """
    Dynamically routes paths between local desktop environments 
    and live deployed Render cloud containers automatically.
    """
    # 1. Checks if running inside an unpacked local desktop executable bundle
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys.__MEIPASS
    else:
        # 2. Falls back to standard root repository matching for live web servers
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    template_path = os.path.join(base_path, "templates", "index.html")
    
    if not os.path.exists(template_path):
        raise HTTPException(
            status_code=404, 
            detail=f"HTML template missing. Looking at target path: {template_path}"
        )
        
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

# Your existing POST generation route
@app.post("/generate-assignments/")
def generate_assignments(payload: dict):
    try:
        if not os.path.exists(EMPLOYEE_FILE):
            return {"status": "error", "detail": f"Missing input file: {EMPLOYEE_FILE}"}
            
        employees = CSVHandler.read_employees_list(EMPLOYEE_FILE)
        
        previous_assignments = {}
        if os.path.exists(PREVIOUS_ASSIGNMENTS_FILE):
            previous_assignments = CSVHandler.read_historical_map(PREVIOUS_ASSIGNMENTS_FILE)
        
        matcher = SecretSantaMatcher(employees, previous_assignments)
        assignments = matcher.assign()
        
        CSVHandler.write_assignments_out(OUTPUT_FILE, assignments)
        
        # ===================================================
        # STRUCTURING THE DATA GRID ARRAY PACKAGES FOR FASTAPI
        # ===================================================
        grid_data_payload = []
        for pair in assignments:
            grid_data_payload.append({
                "employee_name": pair.employee.name,
                "employee_email": pair.employee.email,
                "secret_child_name": pair.secret_child.name,
                "secret_child_email": pair.secret_child.email
            })
            
        return {
            "status": "success", 
            "message": "Assignments successfully generated!",
            "assignments": grid_data_payload  # Send the table rows to the front-end grid
        }
        
    except Exception as e:
        return {"status": "error", "detail": str(e)}

# Your existing GET download route
@app.get("/download-assignments/")
def download_assignments():
    """
    This endpoint downloads the generated Secret Santa assignments CSV file directly.
    """
    if not os.path.exists(OUTPUT_FILE):
        raise HTTPException(
            status_code=404, 
            detail="Assignments file not found. Please click Generate first."
        )
    return FileResponse(
        path=OUTPUT_FILE, 
        media_type="text/csv", 
        filename="secret_santa_assignments.csv"
    )

# ===================================================
# 2. YOUR HOMEPAGE ROUTE (Leave this as is below it)
# ===================================================
@app.get("/", response_class=HTMLResponse)
def serve_homepage():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(_file_))
        
    template_path = os.path.join(base_path, "templates", "index.html")
    
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="HTML template file structure missing on instance.")
        
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)