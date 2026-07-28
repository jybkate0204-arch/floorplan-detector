# Floor Plan Object Detection Web Service

DWG 또는 이미지 평면도를 업로드하면 문과 창문을 탐지하는 웹 프로그램입니다.

## Main Features

- DWG, PNG, JPG, JPEG 파일 업로드
- AutoCAD를 이용한 DWG → PDF 변환
- PyMuPDF를 이용한 PDF → PNG 변환
- YOLOv8 기반 Door, Window 객체 탐지
- 탐지 결과 이미지 표시
- 객체별 개수 출력
- CSV 다운로드
- Streamlit frontend와 FastAPI backend 분리

## System Structure

```text
Streamlit Frontend
        ↓
FastAPI Backend
        ↓
DWG Conversion
        ↓
YOLOv8 Detection
        ↓
Detection Result
````

## File Structure

```text
app_custom.py      Streamlit frontend
backend.py         FastAPI backend
converter.py       DWG, PDF conversion
detector.py        YOLO inference
best.pt            pretrained YOLO model
setting.py         Streamlit settings
helper.py          CSV generation
```

## Requirements

* Windows
* Python 3.11
* AutoCAD installed
* DWG To PDF.pc3 plotter available

## Installation

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Run Backend

```powershell
uvicorn backend:app --reload --port 8000
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Run Frontend

Open another terminal and run:

```powershell
streamlit run app_custom.py
```

Frontend:

```text
http://localhost:8501
```

## Processing Pipeline

### Image Input

```text
PNG or JPG
→ FastAPI
→ YOLOv8
→ Detection Result
```

### DWG Input

```text
DWG
→ AutoCAD
→ PDF
→ PNG
→ YOLOv8
→ Detection Result
```

## Model

This project uses a pretrained YOLOv8 model based on the following reference repository:

[https://github.com/sanatladkat/floor-plan-object-detection](https://github.com/sanatladkat/floor-plan-object-detection)

## Current Limitations

* DWG conversion requires AutoCAD on Windows.
* External cloud deployment is limited because the backend depends on local AutoCAD.
* Detection accuracy depends on drawing scale, line style, and floor-plan complexity.
* The current pretrained model mainly detects doors and windows.

```