## ocr-tools

This document is tutorial how to use olmocr endpoint on DeepInfra to parse texts from pdf

# Install requirements

pip install -r requirements.txt

(if linux): sudo apt-get install poppler-utils 
(if macOS): brew install poppler


# Run command

 python3 scrape_pdf.py --model allenai/olmOCR-7B-0725-FP8 --api-key DEEPINFRA_API_KEY --pdf-path horribleocr.pdf

