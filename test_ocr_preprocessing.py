#!/usr/bin/env python3
"""
Test different OCR preprocessing techniques on problematic images
"""

import os
import sys
sys.path.append('src')

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract

def preprocess_image(image_path, method):
    """Apply different preprocessing methods to improve OCR"""
    img = cv2.imread(image_path)
    if img is None:
        return None
    
    if method == "original":
        return img
    
    elif method == "grayscale":
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    elif method == "threshold":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    elif method == "morphology":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = np.ones((1,1), np.uint8)
        return cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    
    elif method == "denoise":
        return cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    
    elif method == "contrast":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.equalizeHist(gray)
    
    elif method == "resize":
        height, width = img.shape[:2]
        return cv2.resize(img, (width*2, height*2), interpolation=cv2.INTER_CUBIC)
    
    return img

def test_ocr_methods(image_path):
    """Test different OCR methods on an image"""
    print(f"\nTesting OCR methods on: {os.path.basename(image_path)}")
    print("-" * 50)
    
    methods = ["original", "grayscale", "threshold", "morphology", "denoise", "contrast", "resize"]
    
    for method in methods:
        try:
            processed_img = preprocess_image(image_path, method)
            if processed_img is None:
                print(f"{method:12}: Failed to process image")
                continue
            
            # Convert to PIL Image for tesseract
            if len(processed_img.shape) == 3:
                pil_img = Image.fromarray(cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB))
            else:
                pil_img = Image.fromarray(processed_img)
            
            # Try different PSM modes
            configs = ["--oem 3 --psm 6", "--oem 3 --psm 3", "--oem 3 --psm 4", "--oem 3 --psm 8"]
            
            best_text = ""
            best_config = ""
            
            for config in configs:
                try:
                    text = pytesseract.image_to_string(pil_img, config=config)
                    if len(text.strip()) > len(best_text.strip()):
                        best_text = text
                        best_config = config
                except:
                    continue
            
            print(f"{method:12}: {repr(best_text[:50])}... (config: {best_config})")
            
        except Exception as e:
            print(f"{method:12}: Error - {e}")

def main():
    # Test on a few problematic images
    test_images = [
        "Products/IMG-20251003-WA0166.jpg",
        "Products/IMG-20251003-WA0014.jpg",
        "Products/IMG-20251003-WA0020.jpg"
    ]
    
    for img_path in test_images:
        if os.path.exists(img_path):
            test_ocr_methods(img_path)
        else:
            print(f"Image not found: {img_path}")

if __name__ == "__main__":
    main()
