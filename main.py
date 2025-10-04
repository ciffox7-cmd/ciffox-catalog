import argparse
import os
from src.ocr_parser import ocr_images_to_products
from src.rate_parser import parse_rate_list
from src.matching import match_products_with_rates
from src.output import write_csv, write_html


def ensure_dir(path: str) -> None:
	os.makedirs(path, exist_ok=True)


def main():
	parser = argparse.ArgumentParser(description="Generate product catalog from images + rate list")
	parser.add_argument("--images_dir", required=True, help="Path to images folder (e.g., Products)")
	parser.add_argument("--rate_list", required=True, help="Path to RATE LIST.pdf")
	parser.add_argument("--out_dir", default="output", help="Output directory")
	parser.add_argument("--force_ocr", action="store_true", help="Re-run OCR even if cache exists")
	args = parser.parse_args()

	ensure_dir(args.out_dir)
	ocr_cache = os.path.join(args.out_dir, "ocr")
	ensure_dir(ocr_cache)
	thumb_dir = os.path.join(args.out_dir, "thumbs")
	ensure_dir(thumb_dir)

	print("[1/4] OCR images ...")
	products = ocr_images_to_products(args.images_dir, ocr_cache, thumb_dir, force=args.force_ocr)
	print(f"  OCR items: {len(products)}")

	print("[2/4] Parse rate list ...")
	rates = parse_rate_list(args.rate_list)
	print(f"  Rate rows: {len(rates)}")

	print("[3/4] Match ...")
	matched = match_products_with_rates(products, rates)
	print(f"  Matched: {sum(1 for m in matched if m.get('matched'))} / {len(matched)}")

	print("[4/4] Write outputs ...")
	csv_path = os.path.join(args.out_dir, "catalog.csv")
	html_path = os.path.join(args.out_dir, "catalog.html")
	write_csv(matched, csv_path)
	write_html(matched, html_path)
	print("Done:", csv_path, html_path)


if __name__ == "__main__":
	main()


