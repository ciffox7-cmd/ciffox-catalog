import os
import json
from typing import Dict, List
from PIL import Image
import pytesseract


def _thumb(src_path: str, thumb_path: str, size=(400, 400)) -> None:
	try:
		with Image.open(src_path) as img:
			img.verify()  # Verify the image is not corrupted
		
		# Reopen the image for thumbnail generation
		with Image.open(src_path) as img:
			img.thumbnail(size)
			img.save(thumb_path)
	except Exception as e:
		print(f"Warning: Could not create thumbnail for {src_path}: {e}")


def _extract_text(image_path: str) -> str:
	config = "--oem 3 --psm 6"
	try:
		# Try to open and verify the image first
		with Image.open(image_path) as img:
			img.verify()  # Verify the image is not corrupted
		
		# Reopen the image for OCR (verify() closes the file)
		with Image.open(image_path) as img:
			text = pytesseract.image_to_string(img, config=config)
		return text
	except Exception as e:
		print(f"Warning: Could not process image {image_path}: {e}")
		return ""


def _parse_text_to_fields(text: str) -> Dict:
	import re
	
	lines = [l.strip() for l in text.splitlines() if l.strip()]
	
	# Initialize the 4 key properties
	article = None
	colour = None
	size = None
	pair = None
	
	# Join all text for better pattern matching
	full_text = " ".join(lines).lower()
	
	# COMPREHENSIVE PATTERN MATCHING FOR ALL VARIATIONS
	
	# 1. EXTRACT ARTICLE - Multiple patterns to catch all variations
	article_patterns = [
		# Standard patterns
		r'article:\s*([^,\n\r]+?)(?:\s|$)',
		r'aaticle:\s*([^,\n\r]+?)(?:\s|$)',
		r'article[^:]*:\s*([^,\n\r]+?)(?:\s|$)',
		# Garbled article patterns
		r'ticle[^:]*:\s*([^,\n\r]+?)(?:\s|$)',  # "ticle:-Runner-04"
		r'articl[^:]*:\s*([^,\n\r]+?)(?:\s|$)',  # partial "articl"
		r'aticl[^:]*:\s*([^,\n\r]+?)(?:\s|$)',   # partial "aticl"
		r'art[^:]*:\s*([^,\n\r]+?)(?:\s|$)',     # "Art-Sktch 7"
		# Sketch patterns anywhere in text
		r'sketch-\d+[^,\n\r]*?(?:\s|$)',
		r'sketch\s*-\s*\d+[^,\n\r]*?(?:\s|$)',
		r'sktch\s*-\s*\d+[^,\n\r]*?(?:\s|$)',    # "Art-Sktch 7"
		# Look for article-like patterns even without colon
		r'(?:^|\s)(article|aaticle|ticle|articl|aticl|art)\s+([^,\n\r]+?)(?:\s|$)',
		# Look for sketch patterns in any context
		r'(?:^|\s)(sketch-\d+[^,\n\r]*?)(?:\s|$)',
		r'(?:^|\s)(sktch\s*\d+[^,\n\r]*?)(?:\s|$)',  # "Art-Sktch 7"
		# Look for runner patterns
		r'runner-\d+[^,\n\r]*?(?:\s|$)',
		r'mukeson-\d+[^,\n\r]*?(?:\s|$)',
		r'safari-\d+[^,\n\r]*?(?:\s|$)',
	]
	
	for pattern in article_patterns:
		match = re.search(pattern, full_text, re.IGNORECASE)
		if match:
			if len(match.groups()) > 1:
				article = match.group(2).strip()  # For patterns with 2 groups
			else:
				article = match.group(1) if match.groups() else match.group(0)
			article = article.strip().replace("— ", "").replace("aaticle", "article")
			# Clean up more aggressively
			article = re.sub(r'[^a-zA-Z0-9\-_\s].*$', '', article)
			if article and len(article) > 2:  # Only accept substantial articles
				break
	
	# 2. EXTRACT COLOUR - Multiple patterns for all variations
	colour_patterns = [
		r'colour:\s*([^,\n\r]+?)(?:\s|$)',
		r'color:\s*([^,\n\r]+?)(?:\s|$)',
		r'col[^:]*:\s*([^,\n\r]+?)(?:\s|$)',
		# Garbled colour patterns
		r'col-[^:]*:\s*([^,\n\r]+?)(?:\s|$)',  # "Col-Wt/Tan"
		r'col\s*-\s*([^,\n\r]+?)(?:\s|$)',     # "Col-Wt/Tan"
		# Look for colour patterns even without colon
		r'(?:^|\s)(colour|color|col)\s+([^,\n\r]+?)(?:\s|$)',
		r'(?:^|\s)(col-[^,\n\r]+?)(?:\s|$)',   # "Col-Wt/Tan"
		# Look for common color patterns
		r'(?:^|\s)([a-z]+(?:\.|/)[a-z]+(?:\.[a-z]+)?)(?:\s|$)',  # patterns like "t.blue", "black/grey"
		r'(?:^|\s)([a-z]+-[a-z]+(?:/[a-z]+)?)(?:\s|$)',  # patterns like "wt/tan", "white/tan"
	]
	
	for pattern in colour_patterns:
		match = re.search(pattern, full_text, re.IGNORECASE)
		if match:
			if len(match.groups()) > 1:
				colour = match.group(2).strip()
			else:
				colour = match.group(1).strip()
			# Clean up more aggressively
			colour = re.sub(r'[^a-zA-Z0-9\-/\.\s].*$', '', colour)
			if colour and len(colour) > 1:  # Only accept substantial colours
				break
	
	# 3. EXTRACT SIZE - Multiple patterns for all variations
	size_patterns = [
		r'size:\s*([^,\n\r]+?)(?:\s|$)',
		r'stze:\s*([^,\n\r]+?)(?:\s|$)',  # "Stze:-6x9 7x10"
		r'ize[^:]*:\s*([^,\n\r]+?)(?:\s|$)',
		r'se[^:]*:\s*([^,\n\r]+?)(?:\s|$)',  # partial "se"
		# Look for size patterns even without colon
		r'(?:^|\s)(size|stze|ize|se)\s+([^,\n\r]+?)(?:\s|$)',
		# Direct size patterns anywhere in text
		r'(\d+x\d+(?:\s+\d+x\d+)*)',  # patterns like "6x9 7x10"
		r'(\d+/\d+(?:-\d+/\d+)*)',   # patterns like "6/9-7/1"
		r'(\d+x\d+)',  # single size like "6x9"
	]
	
	for pattern in size_patterns:
		match = re.search(pattern, full_text, re.IGNORECASE)
		if match:
			if len(match.groups()) > 1:
				size = match.group(2).strip()
			else:
				size = match.group(1).strip()
			# Clean up common OCR errors
			size = size.replace("stze", "size").replace("ize", "size")
			# Clean up more aggressively - remove trailing garbage but keep size patterns
			size = re.sub(r'\s+(poir|pairs?|air|ss|ui|ag|wa).*$', '', size, flags=re.IGNORECASE)
			size = re.sub(r'[^a-zA-Z0-9\-/x\.\s].*$', '', size)
			if size and len(size) > 1:  # Only accept substantial sizes
				break
	
	# 4. EXTRACT PAIR - Multiple patterns for all variations
	pair_patterns = [
		r'pair[^:]*:\s*([^,\n\r]+?)(?:\s|$)',
		r'poir[^:]*:\s*([^,\n\r]+?)(?:\s|$)',
		r'pairs[^:]*:\s*([^,\n\r]+?)(?:\s|$)',
		r'air[^:]*:\s*([^,\n\r]+?)(?:\s|$)',
		r'paie[^:]*:\s*([^,\n\r]+?)(?:\s|$)',  # OCR error "paie"
		# Look for pair patterns even without colon
		r'(?:^|\s)(pair|poir|pairs|air|paie)\s+([^,\n\r]+?)(?:\s|$)',
		# Look for number patterns that might be pairs
		r'(?:^|\s)(\d+)(?:\s|$)',  # simple number patterns
	]
	
	for pattern in pair_patterns:
		match = re.search(pattern, full_text, re.IGNORECASE)
		if match:
			if len(match.groups()) > 1:
				pair = match.group(2).strip()
			else:
				pair = match.group(1).strip()
			# Clean up common OCR errors
			pair = pair.replace("poir", "pair").replace("air", "pair").replace("paie", "pair")
			# Clean up more aggressively
			pair = re.sub(r'[^a-zA-Z0-9\-\.\s].*$', '', pair)
			if pair and len(pair) > 0:  # Accept any pair value
				break
	
	# FALLBACK PATTERNS - If we still don't have properties, try more aggressive patterns
	
	# If no article found, look for any sketch pattern anywhere
	if not article:
		sketch_matches = re.findall(r'sketch-\d+[^,\n\r]*', full_text, re.IGNORECASE)
		if sketch_matches:
			article = sketch_matches[0].strip()
			article = re.sub(r'[^a-zA-Z0-9\-_\s].*$', '', article)
	
	# If still no article, try more aggressive patterns for garbled text
	if not article:
		# Look for any pattern that might be an article
		article_patterns = [
			r'([a-z]+-\d+)',  # patterns like "sketch-07", "article-03"
			r'([a-z]+\d+)',   # patterns like "sketch07", "article03"
			r'(\d+[a-z]+)',   # patterns like "07sketch"
		]
		for pattern in article_patterns:
			match = re.search(pattern, full_text, re.IGNORECASE)
			if match:
				potential_article = match.group(1).strip()
				# Only accept if it looks like an article
				if len(potential_article) > 3 and any(word in potential_article.lower() for word in ['sketch', 'article', 'item', 'product']):
					article = potential_article
					break
	
	# If no colour found, look for common color words with more aggressive patterns
	if not colour:
		# First try the original color word search
		color_words = ['black', 'white', 'grey', 'gray', 'blue', 'red', 'green', 'yellow', 'brown', 'pink', 'purple', 'orange', 't.blue', 't-blue', 'g.grey', 'l.grey']
		for color in color_words:
			if color in full_text:
				# Find the context around this color
				color_match = re.search(r'[^,\n\r]*' + color + r'[^,\n\r]*', full_text, re.IGNORECASE)
				if color_match:
					colour = color_match.group(0).strip()
					colour = re.sub(r'[^a-zA-Z0-9\-/\.\s].*$', '', colour)
					break
		
		# If still no colour, try more aggressive patterns
		if not colour:
			# Look for patterns like "t.blue", "g.grey", etc.
			color_patterns = [
				r'([a-z]\.?[a-z]+)',  # patterns like "t.blue", "g.grey"
				r'([a-z]+/[a-z]+)',  # patterns like "black/grey"
				r'([a-z]+-[a-z]+)',  # patterns like "t-blue"
			]
			for pattern in color_patterns:
				match = re.search(pattern, full_text, re.IGNORECASE)
				if match:
					potential_color = match.group(1).strip()
					# Only accept if it looks like a color
					if len(potential_color) > 2 and any(c in potential_color.lower() for c in ['blue', 'grey', 'black', 'white', 'red', 'green', 'yellow', 'brown', 'pink', 'purple', 'orange']):
						colour = potential_color
						break
	
	# If no size found, look for any number x number pattern
	if not size:
		size_match = re.search(r'\d+x\d+', full_text)
		if size_match:
			size = size_match.group(0)
	
	# If no pair found, look for any number that might be a pair
	if not pair:
		number_match = re.search(r'\b(\d+)\b', full_text)
		if number_match:
			pair = number_match.group(1)
	
	# ULTRA-AGGRESSIVE FALLBACKS for very poor OCR text
	# If we still have very few properties, try to extract anything that looks like data
	
	if not article and len(full_text) > 0:
		# Try to find any word that might be an article name
		words = re.findall(r'\b[a-zA-Z]+\b', full_text)
		for word in words:
			if len(word) > 3 and word.lower() not in ['size', 'pair', 'colour', 'color', 'article', 'sketch', 'runner', 'mukeson', 'safari']:
				article = word
				break
	
	if not colour and len(full_text) > 0:
		# Try to find any word that might be a color
		color_keywords = ['black', 'white', 'grey', 'gray', 'blue', 'red', 'green', 'yellow', 'brown', 'pink', 'purple', 'orange', 'tan', 'navy', 'sky']
		for color in color_keywords:
			if color in full_text:
				colour = color
				break
	
	if not size and len(full_text) > 0:
		# Try to find any pattern that might be a size
		size_patterns = [r'\d+x\d+', r'\d+/\d+', r'\d+-\d+']
		for pattern in size_patterns:
			match = re.search(pattern, full_text)
			if match:
				size = match.group(0)
				break
	
	if not pair and len(full_text) > 0:
		# Try to find any number that might be a pair
		numbers = re.findall(r'\d+', full_text)
		if numbers:
			# Take the first reasonable number (not too large)
			for num in numbers:
				if 1 <= int(num) <= 100:  # Reasonable pair count
					pair = num
					break
	
	# FINAL CLEANUP
	if article:
		article = re.sub(r'^[^a-zA-Z0-9\-]*', '', article)  # Remove leading non-alphanumeric
		article = re.sub(r'[^a-zA-Z0-9\-_\s].*$', '', article)  # Remove trailing garbage
		article = article.strip()
	
	if colour:
		colour = re.sub(r'^[^a-zA-Z0-9\-/]*', '', colour)  # Remove leading non-alphanumeric
		colour = re.sub(r'[^a-zA-Z0-9\-/\.\s].*$', '', colour)  # Remove trailing garbage
		colour = colour.strip()
	
	if size:
		size = re.sub(r'^[^a-zA-Z0-9\-/x]*', '', size)  # Remove leading non-alphanumeric
		size = re.sub(r'[^a-zA-Z0-9\-/x\.\s].*$', '', size)  # Remove trailing garbage
		size = size.strip()
	
	if pair:
		pair = re.sub(r'^[^a-zA-Z0-9\-]*', '', pair)  # Remove leading non-alphanumeric
		pair = re.sub(r'[^a-zA-Z0-9\-\.\s].*$', '', pair)  # Remove trailing garbage
		pair = pair.strip()
	
	# Create description from remaining text
	desc_lines = []
	for line in lines:
		line_lower = line.lower()
		# Skip lines that contain our extracted properties
		skip = False
		if article and article.lower() in line_lower:
			skip = True
		if colour and colour.lower() in line_lower:
			skip = True
		if size and size.lower() in line_lower:
			skip = True
		if pair and pair.lower() in line_lower:
			skip = True
		if not skip and len(line.strip()) > 2:  # Only include substantial lines
			desc_lines.append(line.strip())
	
	description = " ".join(desc_lines) if desc_lines else None
	
	return {
		"article": article,
		"colour": colour, 
		"size": size,
		"pair": pair,
		"name": article,  # Keep for backward compatibility
		"description": description,
		"raw_text": text
	}


def ocr_images_to_products(images_dir: str, cache_dir: str, thumb_dir: str, force: bool=False) -> List[Dict]:
	products: List[Dict] = []
	for fname in sorted(os.listdir(images_dir)):
		if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
			continue
		img_path = os.path.join(images_dir, fname)
		cache_path = os.path.join(cache_dir, f"{os.path.splitext(fname)[0]}.json")
		thumb_path = os.path.join(thumb_dir, fname)

		if not os.path.exists(thumb_path):
			try:
				_thumb(img_path, thumb_path)
			except Exception:
				pass

		if os.path.exists(cache_path) and not force:
			try:
				with open(cache_path, "r", encoding="utf-8") as f:
					data = json.load(f)
					products.append(data)
					continue
			except Exception:
				pass

		text = _extract_text(img_path)
		fields = _parse_text_to_fields(text)
		item = {
			"image": fname,
			"image_path": img_path,
			"thumb": os.path.relpath(thumb_path, start=os.path.dirname(cache_dir)),
			**fields,
		}
		try:
			with open(cache_path, "w", encoding="utf-8") as f:
				json.dump(item, f, ensure_ascii=False, indent=2)
		except Exception:
			pass
		products.append(item)
	return products


