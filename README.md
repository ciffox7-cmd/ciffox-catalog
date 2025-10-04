# Ciffox Product Catalog Generator

This tool extracts product info from `Products/` via OCR, parses pricing from `RATE LIST.pdf`, matches them, and produces a CSV and an HTML catalog with search and filters.

## Prerequisites
- Python 3.9+
- Tesseract OCR installed and available on PATH (or set env `TESSERACT_CMD` to full path of tesseract.exe)
- Poppler (optional, improves PDF parsing on Windows). Add its `bin` to PATH or set `POPPLER_PATH`.

## Setup
- Create venv and install deps:
  - `python -m venv .venv`
  - `. .venv/Scripts/activate` (PowerShell: `.venv\\Scripts\\Activate.ps1`)
  - `pip install -r requirements.txt`

## Usage
- `python main.py --images_dir Products --rate_list "RATE LIST.pdf" --out_dir output`

## Outputs
- `output/catalog.csv` — tabular dataset
- `output/catalog.html` — searchable HTML catalog with thumbnails
- `output/ocr/` — cached OCR JSON per image

## Notes
- Tune OCR parsing in `src/ocr_parser.py` and matching thresholds in `src/matching.py`.
- If PDF tables fail to parse, the script falls back to OCR of PDF pages.

## Troubleshooting
- If Tesseract is not found, set `TESSERACT_CMD` to its executable path.
- For PDF text issues, install Poppler and ensure PATH or `POPPLER_PATH` is set.


