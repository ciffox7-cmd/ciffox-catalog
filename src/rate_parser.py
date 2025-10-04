from typing import List, Dict
import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os


def _parse_tables_with_pdfplumber(pdf_path: str) -> List[Dict]:
	rows: List[Dict] = []
	with pdfplumber.open(pdf_path) as pdf:
		for page in pdf.pages:
			tables = page.extract_tables() or []
			for table in tables:
				# assume first row is header
				if not table:
					continue
				header = [ (c or "").strip() for c in table[0] ]
				for r in table[1:]:
					cells = [ (c or "").strip() for c in r ]
					row = { f"col_{i}": cells[i] if i < len(cells) else "" for i in range(len(header)) }
					row["raw"] = " | ".join(cells)
					rows.append(row)
	return rows


def _fallback_ocr(pdf_path: str) -> List[Dict]:
	rows: List[Dict] = []
	images = convert_from_path(pdf_path)
	for img in images:
		text = pytesseract.image_to_string(img)
		for line in text.splitlines():
			line = line.strip()
			if not line:
				continue
			rows.append({"raw": line})
	return rows


def parse_rate_list(pdf_path: str) -> List[Dict]:
	if not os.path.exists(pdf_path):
		raise FileNotFoundError(pdf_path)
	rows = _parse_tables_with_pdfplumber(pdf_path)
	if rows:
		return rows
	return _fallback_ocr(pdf_path)


