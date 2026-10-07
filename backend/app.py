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
    
    # Clean up temp file (for now just delete after saving)
    os.remove(temp_file_path)
    
    # Dummy response as per plan
    return {
        "markdown_summary": "# Summary",
        "image_url": ""
    }
