from fastapi import FastAPI, UploadFile, File
import logging
import shutil
import os

# Set up session logging for rollback maintenance
logging.basicConfig(
    filename='session.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

@app.post("/api/generate-recap")
async def generate_recap(file: UploadFile = File(...)):
    logging.info(f"Received file: {file.filename}")
    
    # Save it temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    logging.info(f"Temporarily saved file to {temp_file_path}")
    
    from backend.workflow import run_agent_workflow
    result = run_agent_workflow(temp_file_path)
    
    # Clean up temp file
    os.remove(temp_file_path)
    
    return result
