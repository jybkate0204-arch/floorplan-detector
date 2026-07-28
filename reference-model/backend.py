import base64
import io
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from PIL import Image

import converter
import detector


app = FastAPI(title="Floor Plan Detection API")


@app.get("/")
def health_check():
    return {
        "message": "Floor Plan Detection Backend is running."
    }


@app.post("/detect")
async def detect(
    file: UploadFile = File(...),
    confidence: float = Form(0.4),
    labels: str = Form("Door,Window"),
):
    try:
        filename = file.filename or "uploaded_file"
        extension = Path(filename).suffix.lower()
        file_bytes = await file.read()

        selected_labels = [
            label.strip()
            for label in labels.split(",")
            if label.strip()
        ]

        if extension == ".dwg":
            with tempfile.TemporaryDirectory() as temp_directory:
                temp_path = Path(temp_directory)

                dwg_path = temp_path / "uploaded.dwg"
                pdf_path = temp_path / "converted.pdf"
                png_path = temp_path / "converted.png"

                dwg_path.write_bytes(file_bytes)

                converter.convert_dwg_to_pdf(
                    str(dwg_path),
                    str(pdf_path),
                )

                converter.convert_pdf_to_png(
                    str(pdf_path),
                    str(png_path),
                )

                image = Image.open(png_path).convert("RGB")

        elif extension in {".png", ".jpg", ".jpeg"}:
            image = Image.open(
                io.BytesIO(file_bytes)
            ).convert("RGB")

        else:
            raise HTTPException(
                status_code=400,
                detail="Only DWG, PNG, JPG, and JPEG files are supported.",
            )

        annotated_image, counts, _ = detector.detect_objects(
            image=image,
            confidence=confidence,
            selected_labels=selected_labels,
        )

        output_buffer = io.BytesIO()

        Image.fromarray(annotated_image).save(
            output_buffer,
            format="PNG",
        )

        encoded_image = base64.b64encode(
            output_buffer.getvalue()
        ).decode("utf-8")

        return {
            "filename": filename,
            "input_type": extension,
            "counts": counts,
            "annotated_image": encoded_image,
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        ) from error