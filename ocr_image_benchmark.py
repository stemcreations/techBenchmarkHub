#!/usr/bin/env python3
"""
Specialized OCR for Tom's Hardware style benchmark charts
Handles horizontal bar charts with multiple data points
"""

import cv2
import pytesseract
import pandas as pd
import re
import numpy as np
from typing import List, Tuple, Dict

def preprocess_chart_image(image_path: str) -> np.ndarray:
    """
    Preprocess chart image with specific optimizations for bar charts
    """
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Increase contrast for better text recognition
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Apply threshold to separate text from background
    _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    return thresh

def extract_chart_regions(image_path: str) -> Dict:
    """
    Extract text from different regions of the chart
    """
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    
    # Define regions (you may need to adjust these ratios)
    left_region = img[:, :int(width * 0.2)]  # GPU names area
    right_region = img[:, int(width * 0.7):]  # Right-side numbers area
    center_region = img[:, int(width * 0.2):int(width * 0.7)]  # Bar area
    
    regions = {
        'left': left_region,
        'right': right_region, 
        'center': center_region,
        'full': img
    }
    
    extracted_text = {}
    for region_name, region_img in regions.items():
        # Convert to grayscale and preprocess
        gray = cv2.cvtColor(region_img, cv2.COLOR_BGR2GRAY)
        
        if region_name == 'center':
            # For center region (bars), try to extract white text on colored background
            # Invert image to make white text black
            inverted = cv2.bitwise_not(gray)
            processed = inverted
        else:
            # For other regions, use normal processing
            _, processed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # OCR configuration for better number recognition
        config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,()[]/-+: '
        text = pytesseract.image_to_string(processed, config=config)
        extracted_text[region_name] = text
    
    return extracted_text

def parse_gpu_chart(extracted_text: Dict, chart_title: str = "") -> List[Dict]:
    """
    Parse GPU benchmark chart with horizontal bars
    """
    results = []
    
    # Extract GPU names from left region
    left_text = extracted_text.get('left', '')
    gpu_names = []
    
    # GPU name patterns
    gpu_patterns = [
        r'RTX\s*\d+\s*(?:Ti\s*)?(?:Super\s*)?(?:\d+GB)?',
        r'RX\s*\d+\s*(?:XT|XTX)?',
        r'Arc\s*[AB]\d+',
        r'GTX\s*\d+\s*(?:Ti\s*)?'
    ]
    
    lines = left_text.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
        for pattern in gpu_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                gpu_names.append(line)
                break
    
    # Extract numbers from right region (1% Low values)
    right_text = extracted_text.get('right', '')
    right_numbers = re.findall(r'\b(\d+\.?\d*)\b', right_text)
    
    # Extract numbers from center region (Average FPS)
    center_text = extracted_text.get('center', '')
    center_numbers = re.findall(r'\b(\d+\.?\d*)\b', center_text)
    
    # Also try full image OCR as backup
    full_text = extracted_text.get('full', '')
    
    print(f"Found {len(gpu_names)} GPU names")
    print(f"Found {len(right_numbers)} right-side numbers")
    print(f"Found {len(center_numbers)} center numbers")
    
    # Try to match GPU names with numbers
    # This is the tricky part - we need to align the data correctly
    for i, gpu_name in enumerate(gpu_names):
        avg_fps = None
        low_fps = None
        
        # Try to get corresponding numbers
        if i < len(center_numbers):
            avg_fps = center_numbers[i]
        if i < len(right_numbers):
            low_fps = right_numbers[i]
        
        # Also try to find numbers in the same line in full text
        full_lines = full_text.split('\n')
        for line in full_lines:
            if gpu_name.lower() in line.lower():
                line_numbers = re.findall(r'\b(\d+\.?\d*)\b', line)
                if len(line_numbers) >= 2:
                    avg_fps = line_numbers[0]  # First number (in bar)
                    low_fps = line_numbers[1]   # Second number (on right)
                elif len(line_numbers) == 1:
                    if not avg_fps:
                        avg_fps = line_numbers[0]
                break
        
        if avg_fps or low_fps:
            results.append({
                'GPU_Model': gpu_name,
                'Date': '[extracted]',
                'AVG_FPS': avg_fps,
                '1%_Low': low_fps,
                '0.1%_Low': None
            })
    
    return results

def extract_from_benchmark_chart(image_path: str, output_file: str = None) -> pd.DataFrame:
    """
    Main function to extract data from benchmark chart
    """
    print(f"Processing benchmark chart: {image_path}")
    
    # Extract text from different regions
    extracted_text = extract_chart_regions(image_path)
    
    # Parse the chart data
    results = parse_gpu_chart(extracted_text)
    
    if not results:
        print("No data extracted. Showing raw OCR output for debugging:")
        for region, text in extracted_text.items():
            print(f"\n--- {region.upper()} REGION ---")
            print(text[:300] + "..." if len(text) > 300 else text)
        return pd.DataFrame()
    
    # Create DataFrame
    df = pd.DataFrame(results)
    
    # Clean up the data
    df = df.dropna(subset=['GPU_Model'])
    
    # Convert numeric columns
    for col in ['AVG_FPS', '1%_Low']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print(f"Extracted {len(df)} results:")
    print(df)
    
    if output_file:
        df.to_csv(output_file, index=False)
        print(f"Saved to {output_file}")
    
    return df

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python chart_ocr.py <image_path> [output_file]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    extract_from_benchmark_chart(image_path, output_file)