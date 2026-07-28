from pathlib import Path

from PIL import Image
from ultralytics import YOLO


MODEL_PATH = Path(__file__).with_name("best.pt")
_model = YOLO(str(MODEL_PATH))


def detect_objects(
    image: Image.Image,
    confidence: float,
    selected_labels: list[str],
):
    """Run YOLO detection and return the annotated image, counts, and results."""
    results = _model.predict(image, conf=confidence)
    result = results[0]

    selected = set(selected_labels)
    filtered_boxes = [
        box
        for box in result.boxes
        if _model.names[int(box.cls.item())] in selected
    ]
    result.boxes = filtered_boxes

    counts: dict[str, int] = {}
    for box in filtered_boxes:
        label = _model.names[int(box.cls.item())]
        counts[label] = counts.get(label, 0) + 1

    annotated_image = result.plot(
    line_width=1,
    font_size=8,
)[:, :, ::-1]
    return annotated_image, counts, result