#!/usr/bin/env python3

# pip install pytesseract pdf2image PyPDF2
# brew install tesseract

import logging
from pathlib import Path
import io

import pytesseract
from pdf2image import convert_from_path
import PyPDF2

FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(
    format=FORMAT,
    datefmt="%Y-%m-%dT%H:%M:%S",
    # logger levels are: DEBUG, INFO, WARNING, ERROR, CRITICAL
    level=os.environ.get('LOGLEVEL', 'INFO').upper(),
)
logger = logging.getLogger()

def main():
    exec = Path(__name__)
    p = Path()
    logger.info(f"Run {str(exec)} on {str(p)}")

    # Recursive glob on PDF files
    # for pdf_path in sorted(Path().rglob("*.pdf")):

    # Local glob on PDF files
    for pdf_path in sorted(Path().glob("*.pdf")):
        filename = str(pdf_path)
        images = convert_from_path(filename, 500)
        pdf_writer = PyPDF2.PdfWriter()
        logger.info(f"Start {filename}: {len(images)} pages")

        for i, image in enumerate(images, start=1):
            page = pytesseract.image_to_pdf_or_hocr(image, extension='pdf')
            _bytes = io.BytesIO(page)
            pdf = PyPDF2.PdfReader(_bytes)
            pdf_writer.add_page(pdf.pages[0])
            pdf = None
            logger.info(f"\tpage {i}")

        out_filename = f"search-{filename}"
        with open(out_filename, "wb") as f:
            pdf_writer.write(f)

        logger.info(f"End {filename}")


if __name__ == '__main__':
    main()
