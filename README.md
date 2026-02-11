
# 🚗 License Plate Recognition System

A full-stack computer vision web application that detects vehicle license plates using **YOLOv8**, extracts text via **EasyOCR**, classifies **Indian license plate colours**, infers **vehicle type**, and logs results into a **CSV file**.

---

## 📌 Project Overview

This project combines **Deep Learning**, **OCR**, and **Web Development** to build an automated License Plate Recognition (LPR) system.

Users can upload a vehicle image through a **React.js frontend**, which sends the image to a **Flask backend API**. The backend performs:

1. License plate detection (YOLOv8)
2. Text recognition (EasyOCR)
3. Colour classification (OpenCV + HSV)
4. Vehicle type inference
5. CSV logging

The results are returned to the frontend and displayed instantly.

---

## 🧠 How the System Works

### **Step 1 — Image Upload**
User selects an image from the React UI.

⬇  
Frontend → sends image via Axios → Flask API

---

### **Step 2 — Plate Detection (YOLOv8)**

YOLOv8 identifies bounding boxes around license plates.

✔ Fast object detection  
✔ High accuracy  
✔ Real-time capable  

Output:
- Coordinates of detected plate
- Confidence score

---

### **Step 3 — Plate Cropping**

Detected region is cropped using OpenCV:

```python
plate_img = img[y1:y2, x1:x2]
````

---

### **Step 4 — Text Extraction (EasyOCR)**

EasyOCR reads characters from the cropped plate.

✔ Deep learning-based OCR
✔ Works on noisy images

Output:

* Plate number text

---

### **Step 5 — Colour Detection**

The plate image is converted to **HSV colour space**:

```python
hsv = cv2.cvtColor(plate_img, cv2.COLOR_BGR2HSV)
```

HSV ranges detect:

| Colour | Meaning                |
| ------ | ---------------------- |
| White  | Private vehicle        |
| Yellow | Commercial vehicle     |
| Green  | Electric vehicle       |
| Red    | Temporary registration |

The colour with the highest pixel count is selected.

---

### **Step 6 — Vehicle Type Inference**

Colour → mapped to vehicle category:

```python
White  → Private
Yellow → Commercial
Green  → Electric
Red    → Temporary
```

---

### **Step 7 — CSV Logging**

Each detection is saved:

| filename | plate_text | colour | vehicle_type | confidence |
| -------- | ---------- | ------ | ------------ | ---------- |

Stored in:

```
backend/results.csv
```

---

## 🛠 Tech Stack

### **Frontend**

* React.js
* Axios
* CSS

### **Backend**

* Flask
* Flask-CORS
* Ultralytics YOLOv8
* EasyOCR
* OpenCV
* NumPy

---

## 🏗 Architecture

```
React Frontend  →  Flask API  →  YOLOv8 + OCR + OpenCV
```

**Flow:**

User → Upload Image → Backend Processing → JSON Response → UI Display

---

## 📂 Project Structure

```
licence_plate_project/
│
├── frontend/              # React Application
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/               # Flask API
│   ├── app.py
│   ├── model/
│   │    └── license_plate_detector.pt
│   └── results.csv
│
└── README.md
```

---

## ⚙️ Installation & Setup

---

### 🔹 **Backend Setup (Flask)**

```bash
cd backend
pip install -r requirements.txt
python app.py
```

Runs on:

```
http://localhost:5001
```

---

### 🔹 **Frontend Setup (React)**

```bash
cd frontend
npm install
npm start
```

Runs on:

```
http://localhost:3000
```

---

## 📡 API Endpoints

| Endpoint        | Method | Description                      |
| --------------- | ------ | -------------------------------- |
| `/detect`       | POST   | Upload image for plate detection |
| `/download_csv` | GET    | Download CSV results             |

---

## 📊 Output Example

For each detected plate:

✔ Plate Number
✔ Plate Colour
✔ Vehicle Type
✔ Confidence Score

---

## 🚀 Deployment Notes

* **Frontend:** Netlify / Vercel
* **Backend:** Render / Railway / VPS

⚠ Netlify hosts static frontend only.

---

## ⚠ Limitations

* OCR accuracy depends on image quality
* Multiple plates may overlap
* Colour detection affected by lighting
* CPU inference slower than GPU

---

## 🔮 Future Improvements

✔ Live webcam detection
✔ Multi-plate UI visualization
✔ Better OCR filtering
✔ Model optimisation
✔ Dark mode UI

---

## 👩‍💻 Author

**Sowndaryaa Rameshbabu**
BE Computer Science Engineering

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub!

```

---

---


