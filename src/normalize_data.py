"""
This file extracts each page of a PDF file as an image and saves it to the data dir.
"""

from pathlib import Path
import pymupdf

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

for pdf_file in DATA_DIR.iterdir():
    # Assumes a flat file structure inside of dir
        
    doc = pymupdf.open(pdf_file)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=200)
        pix.save(DATA_DIR / f"{i+1:03d}.jpeg")

