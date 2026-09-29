from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from src.orchestrator import Orchestrator
from src.document_annotator import annotate_pdf

import shutil
import os

# Ensure necessary directories exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app = FastAPI(title="DocIntel API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# orchestrator
orchestrator = Orchestrator()

@app.get("/")
def health_check():
    return {"status": "DocIntel API is running"}

@app.post("/analyze")
async def analyze_report(
    file: UploadFile = File(...),
    project_type: str = Form(default="residential"),
    city_tier: str = Form(default="tier_2")
):
    os.makedirs("uploads", exist_ok=True)
    # Save uploaded file
    upload_path = f"uploads/{file.filename}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run pipeline
    result = orchestrator.process(upload_path, project_type, city_tier)

    # Cleanup uploaded file
    if os.path.exists(upload_path):
        os.remove(upload_path)

    return result

@app.post("/analyze-and-annotate")
async def analyze_and_annotate(
    file: UploadFile = File(...),
    project_type: str = Form(default="residential"),
    city_tier: str = Form(default="tier_2")
):
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)

    # Save upload
    upload_path = f"uploads/{file.filename}"
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run pipeline
    result = orchestrator.process(upload_path, project_type, city_tier)

    # Annotate PDF
    output_path = f"outputs/annotated_{file.filename}"
    annotate_pdf(upload_path, output_path, result["agents"])

    # Cleanup upload
    if os.path.exists(upload_path):
        os.remove(upload_path)

    result["annotated_filename"] = file.filename
    return result

@app.get("/download/{filename}")
def download_annotated(filename: str):
    path = f"outputs/annotated_{filename}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, media_type="application/pdf", filename=f"DocIntel_{filename}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
