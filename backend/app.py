import sys
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from ultralytics import YOLO
import cv2
import easyocr
import numpy as np
import csv
import os

# --- Flask Setup ---
app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "OPTIONS"])

# --- YOLO and OCR Setup ---
MODEL_PATH = "model/license_plate_detector.pt"
model = YOLO(MODEL_PATH, task="detect")
reader = easyocr.Reader(['en'], gpu=False)

# --- CSV Setup ---
CSV_FILE = "results.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "plate_text", "colour", "vehicle_type", "confidence"])

# --- Helper Functions ---
def detect_plate_colour(plate_img):
    hsv = cv2.cvtColor(plate_img, cv2.COLOR_BGR2HSV)
    ranges = {
        "White": ([0, 0, 200], [180, 40, 255]),
        "Yellow": ([15, 80, 80], [40, 255, 255]),
        "Green": ([35, 50, 50], [85, 255, 255]),
        "Red": ([0, 70, 50], [10, 255, 255])
    }
    pixel_counts = {}
    for color, (low, high) in ranges.items():
        mask = cv2.inRange(hsv, np.array(low), np.array(high))
        pixel_counts[color] = cv2.countNonZero(mask)
    return max(pixel_counts, key=pixel_counts.get)

def vehicle_type_from_colour(colour):
    mapping = {
        "White": "Private",
        "Yellow": "Commercial",
        "Green": "Electric",
        "Red": "Temporary"
    }
    return mapping.get(colour, "Unknown")

def process_image_file(image_path):
    """Process local image file like HTTP POST"""
    filename = os.path.basename(image_path)
    img = cv2.imread(image_path)

    results = model.predict(img, imgsz=640)[0]
    detections = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])

        plate_img = img[y1:y2, x1:x2]
        ocr_result = reader.readtext(plate_img)
        plate_text = ocr_result[0][1] if ocr_result else "UNKNOWN"

        colour = detect_plate_colour(plate_img)
        vehicle_type = vehicle_type_from_colour(colour)

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([filename, plate_text, colour, vehicle_type, round(conf, 2)])

        detections.append({
            "text": plate_text,
            "colour": colour,
            "vehicle_type": vehicle_type,
            "confidence": round(conf, 2)
        })

    print(f"Detections for {filename}:")
    for d in detections:
        print(d)


# --- Flask Routes (unchanged) ---
@app.route("/detect", methods=["POST"])
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    filename = file.filename
    img_bytes = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

    results = model.predict(img, imgsz=640)[0]
    detections = []

    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        plate_img = img[y1:y2, x1:x2]
        ocr_result = reader.readtext(plate_img)
        plate_text = ocr_result[0][1] if ocr_result else "UNKNOWN"
        colour = detect_plate_colour(plate_img)
        vehicle_type = vehicle_type_from_colour(colour)

        with open(CSV_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([filename, plate_text, colour, vehicle_type, round(conf, 2)])

        detections.append({
            "text": plate_text,
            "colour": colour,
            "vehicle_type": vehicle_type,
            "confidence": round(conf, 2)
        })

    return jsonify(detections), 200

@app.route("/download_csv", methods=["GET"])
def download_csv():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True)
    else:
        return jsonify({"error": "CSV file not found"}), 404

# --- Main ---
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run local test with image
        image_path = sys.argv[1]
        if os.path.exists(image_path):
            process_image_file(image_path)
        else:
            print("Image not found:", image_path)
    else:
        # Run Flask server
        app.run(debug=True, host="0.0.0.0", port=5001)
