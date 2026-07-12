import sys
import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from services.csv_handler import CSVHandler
from services.matcher import SecretSantaMatcher

# Initialize the FastAPI app framework
app = FastAPI(title="Secret Santa Matcher API")

@app.get("/")
def read_root():
    return {"status": "Server is running!", "message": "Go to /run-matcher to generate your Secret Santa list."}

@app.get("/run-matcher")
def run_matcher():
    try:
        # Load your data registries
        employees = CSVHandler.load_employees('employees.csv')
        history = CSVHandler.load_history('previous_assignments.csv')
        
        # Run the assignment algorithms
        matcher = SecretSantaMatcher(employees, history)
        results = matcher.generate_assignments()
        
        # Save output assignments
        CSVHandler.save_assignments('secret_santa_output.csv', results)
        
        return JSONResponse(content={
            "status": "Success",
            "message": "Successfully generated secret_santa_output.csv",
            "assignments_count": len(results)
        }, status_code=200)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Operational Execution Error: {str(e)}")

if __name__== "__main__":
    # Render maps network bindings dynamically using environmental port tags
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)