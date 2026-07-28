from pathlib import Path
import time

import fitz
import pythoncom
import win32com.client


def convert_dwg_to_pdf(dwg_path: str, output_pdf_path: str) -> str:
    """AutoCAD를 이용해 DWG의 Model Space 전체 영역을 PDF로 변환한다."""

    dwg_file = Path(dwg_path).resolve()
    pdf_file = Path(output_pdf_path).resolve()

    if not dwg_file.exists():
        raise FileNotFoundError(f"DWG file not found: {dwg_file}")

    pdf_file.parent.mkdir(parents=True, exist_ok=True)

    pythoncom.CoInitialize()

    autocad = win32com.client.Dispatch("AutoCAD.Application")
    autocad.Visible = True

    document = None

    try:
        document = autocad.Documents.Open(str(dwg_file))
        time.sleep(2)

        # 백그라운드 출력 방지
        document.SetVariable("BACKGROUNDPLOT", 0)

        layout = document.ModelSpace.Layout

        # PDF 출력 장치
        layout.ConfigName = "DWG To PDF.pc3"

        # 도면 전체 영역 출력
        layout.PlotType = 1  # acExtents
        layout.CenterPlot = True
        layout.UseStandardScale = True
        layout.StandardScale = 0  # acScaleToFit

        document.Regen(1)

        success = document.Plot.PlotToFile(
            str(pdf_file),
            "DWG To PDF.pc3",
        )

        if not success or not pdf_file.exists():
            raise RuntimeError("AutoCAD PDF conversion failed.")

        return str(pdf_file)

    finally:
        if document is not None:
            document.Close(False)

        pythoncom.CoUninitialize()
        import fitz


def convert_pdf_to_png(pdf_path: str, output_png_path: str) -> str:
    pdf_file = Path(pdf_path).resolve()
    png_file = Path(output_png_path).resolve()

    if not pdf_file.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_file}")

    png_file.parent.mkdir(parents=True, exist_ok=True)

    document = fitz.open(str(pdf_file))
    page = document.load_page(0)

    matrix = fitz.Matrix(2, 2)
    pixmap = page.get_pixmap(matrix=matrix, alpha=False)
    pixmap.save(str(png_file))

    document.close()

    return str(png_file)