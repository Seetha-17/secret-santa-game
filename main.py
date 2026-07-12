import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
from services.csv_handler import CSVHandler
from services.matcher import SecretSantaMatcher

# Title updated to Secret Santa Game
app = FastAPI(title="Secret Santa Game")

# Define the Request Body structure
class AssignmentRequest(BaseModel):
    current_year_file: str
    previous_year_file: Optional[str] = None

# POST endpoint for generating assignments
@app.post("/generate-assignments/", summary="Generate Assignments")
def generate_assignments(request: AssignmentRequest):
    try:
        # Use the file names provided by the user in the form input
        employees_file = request.current_year_file
        history_file = request.previous_year_file if request.previous_year_file else 'previous_assignments.csv'
        
        # Verify files exist on the server before trying to read them
        if not os.path.exists(employees_file):
            raise HTTPException(status_code=400, detail=f"File not found: {employees_file}")
            
        # Load your data registries
        employees = CSVHandler.load_employees(employees_file)
        history = CSVHandler.load_history(history_file) if os.path.exists(history_file) else []
        
        # Run the assignment algorithms
        matcher = SecretSantaMatcher(employees, history)
        results = matcher.generate_assignments()
        
        # Save output assignments
        output_path = 'secret_santa_output.csv'
        CSVHandler.save_assignments(output_path, results)
        
        return JSONResponse(content={
            "status": "Success",
            "message": f"Successfully generated {output_path}",
            "assignments_count": len(results)
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Operational Execution Error: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)