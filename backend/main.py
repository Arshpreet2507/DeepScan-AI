from fastapi import FastAPI, File, UploadFile
import shutil
import os
from .inference import predict_video

app = FastAPI(title="TrustLens 2026 API")

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    label, confidence = predict_video(file_path)

    # Cleanup temp file
    os.remove(file_path)

    return {
        "prediction": label,
        "confidence": confidence
    }