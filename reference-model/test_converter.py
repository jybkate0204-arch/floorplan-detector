from converter import convert_dwg_to_pdf, convert_pdf_to_png


pdf_path = convert_dwg_to_pdf(
    "test.dwg",
    "output/test.pdf",
)

png_path = convert_pdf_to_png(
    pdf_path,
    "output/test.png",
)

print("PDF 완료:", pdf_path)
print("PNG 완료:", png_path)