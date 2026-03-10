import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from mtcnn.mtcnn import MTCNN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "trustlens_model_v1.h5")

model = load_model(MODEL_PATH)
detector = MTCNN()

def predict_video(video_path, threshold=0.5, frame_skip=15):
    cap = cv2.VideoCapture(video_path)
    preds = []
    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_id % frame_skip == 0:
            faces = detector.detect_faces(frame)

            for face in faces:
                x, y, w, h = face['box']
                x, y = max(0, x), max(0, y)
                face_img = frame[y:y+h, x:x+w]

                if face_img.size == 0:
                    continue

                face_img = cv2.resize(face_img, (224, 224))
                face_img = face_img / 255.0
                face_img = np.expand_dims(face_img, axis=0)

                pred = model.predict(face_img, verbose=0)[0][0]
                preds.append(pred)

        frame_id += 1

    cap.release()

    if len(preds) == 0:
        return "NO FACE DETECTED", 0.0

    avg_score = float(np.mean(preds))
    label = "FAKE" if avg_score > threshold else "REAL"

    return label, round(avg_score, 4)