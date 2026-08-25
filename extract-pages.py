#!/usr/bin/env python3

"""
Convert a PDF into extracted page images (PNG format)
without using pdf2image.

Images are saved with 10 leading zeros:
    0000000001.png
    0000000002.png
    ...
"""

from tqdm import tqdm
import sys
import os
from pathlib import Path
import fitz  # PyMuPDF


def pdf_to_images(pdf_path: str, output_dir: str, dpi: int = 300):
    """
    Convert each page of a PDF to an image.

    Args:
        pdf_path: Path to input PDF
        output_dir: Directory to save images
        dpi: Rendering resolution (default 300)
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    output_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)

    # Scale factor from DPI (default PDF is 72 DPI)
    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    for page_index in tqdm(range(len(doc))):
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=matrix)

        filename = f"{page_index + 1:010d}.png"
        output_path = output_dir / filename

        pix.save(output_path)
        print(f"Saved: {output_path}")

    doc.close()


def main():
    if len(sys.argv) < 3:
        print("Usage: python pdf_to_images.py input.pdf output_directory [dpi]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300

    pdf_to_images(pdf_path, output_dir, dpi)


if __name__ == "__main__":
    main()

