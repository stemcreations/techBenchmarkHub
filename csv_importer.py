import pandas as pd
import re
from models import app, db, Product, BenchmarkCategory, BenchmarkResult

def parse_product_name(full_name):
    """
    Extract clean product name and core count from full name
    Examples:
    - "AMD R7 9700X Lexar 6000" -> ("AMD R7 9700X", None)
    - "Intel i9-14900K" -> ("Intel i9-14900K", None)
    """
    # Remove extra specs like "Lexar 6000", memory configs, etc.
    clean_name = re.sub(r'\s+Lexar\s+\d+', '', full_name)
    clean_name = re.sub(r'\s+DDR\d+-\d+', '', clean_name)
    clean_name = clean_name.strip()
    
    return clean_name

def detect_product_type(product_name):
    """
    Determine if product is CPU or GPU based on name
    """
    cpu_indicators = ['AMD R', 'Intel i', 'Intel Core', 'Intel Pentium', 'Intel Celeron']
    gpu_indicators = ['RTX', 'GTX', 'RX ', 'Arc', 'Radeon']
    
    name_upper = product_name.upper()
    
    for indicator in gpu_indicators:
        if indicator.upper() in name_upper:
            return 'GPU'
    
    for indicator in cpu_indicators:
        if indicator.upper() in name_upper:
            return 'CPU'
    
    # Default to CPU if unclear
    return 'CPU'

def import_csv(csv_file_path, benchmark_name, benchmark_description="", unit_type="score", resolution=None, default_date=None):
    """
    Import CSV data into database
    Supports both CPU format (CPU_Model, Core_Count, Date, Score) 
    and GPU format (GPU_Model, Date, AVG_FPS, 1%_Low, 0.1%_Low)
    
    Args:
        csv_file_path: Path to CSV file
        benchmark_name: Name of the benchmark (e.g., "Adobe Photoshop Puget Suite" or "Starfield CPU Performance")
        benchmark_description: Optional description
        unit_type: Type of measurement (score, fps, seconds, etc.)
        resolution: Resolution for gaming benchmarks ('1080p', '1440p', '4K') - applies to both CPU and GPU gaming tests
        default_date: Default date to use if Date column is missing (format: '[M/YY]' e.g., '[9/25]')
    """
    
    with app.app_context():
        # Read CSV
        try:
            df = pd.read_csv(csv_file_path)
            print(f"Loaded {len(df)} rows from {csv_file_path}")
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return False
        
        # Detect CSV format and validate
        is_gpu_format = False
        has_date_column = 'Date' in df.columns
        
        # Check for GPU format columns (Date is now optional)
        gpu_columns_required = ['GPU_Model', 'AVG_FPS', '1%_Low']
        gpu_columns_optional = ['GPU_Model', 'Date', 'AVG_FPS', '1%_Low']
        
        if all(col in df.columns for col in gpu_columns_required):
            is_gpu_format = True
            product_col = 'GPU_Model'
            score_col = 'AVG_FPS'
            core_count_col = None
            print("Detected GPU CSV format")
        else:
            # Check for CPU format columns (Date is now optional)
            cpu_columns_required = ['CPU_Model', 'Core_Count', 'Score']
            cpu_columns_optional = ['CPU_Model', 'Core_Count', 'Date', 'Score']
            
            if not all(col in df.columns for col in cpu_columns_required):
                print(f"CSV must have either:")
                print(f"  GPU columns: {gpu_columns_optional} (Date optional)")
                print(f"  CPU columns: {cpu_columns_optional} (Date optional)")
                return False
            product_col = 'CPU_Model'
            score_col = 'Score'
            core_count_col = 'Core_Count'
            print("Detected CPU CSV format")
        
        # Handle missing Date column
        if not has_date_column:
            if default_date:
                print(f"No Date column found. Using provided default date: {default_date}")
                df['Date'] = default_date
            else:
                # Ask user for date input
                while True:
                    user_date = input("No Date column found in CSV. Please enter a date (format [M/YY], e.g., [9/25]): ").strip()
                    if user_date.startswith('[') and user_date.endswith(']') and '/' in user_date:
                        df['Date'] = user_date
                        print(f"Using date: {user_date}")
                        break
                    else:
                        print("Invalid format. Please use format [M/YY] like [9/25]")
        else:
            print(f"Found Date column in CSV")
        
        # Determine product type from first few entries
        sample_names = df[product_col].head(3).tolist()
        product_type = detect_product_type(sample_names[0])
        print(f"Detected product type: {product_type}")
        
        # Create unique benchmark name including resolution for gaming benchmarks
        full_benchmark_name = benchmark_name
        if resolution:
            full_benchmark_name = f"{benchmark_name} {resolution}"
        
        # Create or get benchmark category
        category = BenchmarkCategory.query.filter_by(name=full_benchmark_name).first()
        if not category:
            category = BenchmarkCategory(
                name=full_benchmark_name,
                description=benchmark_description,
                unit_type=unit_type,
                product_type=product_type,
                resolution=resolution
            )
            db.session.add(category)
            db.session.commit()
            print(f"Created benchmark category: {full_benchmark_name}")
        
        # Process each row
        products_added = 0
        results_added = 0
        
        for _, row in df.iterrows():
            # Parse product info
            full_name = row[product_col]
            clean_name = parse_product_name(full_name)
            
            # Get core count if available (CPU format)
            core_count = row[core_count_col] if core_count_col else None
            
            test_date = row['Date']
            score = float(row[score_col])
            
            # Get 1% low score if available (GPU format only)
            score_1_percent_low = None
            if is_gpu_format and '1%_Low' in df.columns:
                score_1_percent_low = float(row['1%_Low'])
            
            # Create or get product
            product = Product.query.filter_by(name=clean_name).first()
            if not product:
                product = Product(
                    name=clean_name,
                    type=product_type,
                    core_count=core_count
                )
                db.session.add(product)
                db.session.commit()
                products_added += 1
                print(f"Added product: {clean_name}")
            
            # Create or update benchmark result
            existing_result = BenchmarkResult.query.filter_by(
                product_id=product.id,
                category_id=category.id
            ).first()
            
            if existing_result:
                # Ask user what to do with duplicate data
                print(f"\nDuplicate found for {clean_name} in {full_benchmark_name}")
                print(f"  Existing: {existing_result.score}" + 
                      (f" (1% low: {existing_result.score_1_percent_low})" if existing_result.score_1_percent_low else "") +
                      f" Date: {existing_result.test_date}")
                print(f"  New data: {score}" + 
                      (f" (1% low: {score_1_percent_low})" if score_1_percent_low else "") +
                      f" Date: {test_date}")
                
                while True:
                    choice = input("What would you like to do? (u)pdate existing / (s)kip new data / (q)uit import: ").lower().strip()
                    if choice == 'u':
                        existing_result.score = score
                        existing_result.score_1_percent_low = score_1_percent_low
                        existing_result.test_date = test_date
                        print(f"✓ Updated result for {clean_name}")
                        break
                    elif choice == 's':
                        print(f"✓ Skipped new data for {clean_name}")
                        break
                    elif choice == 'q':
                        print("Import cancelled by user")
                        return False
                    else:
                        print("Invalid choice. Please enter 'u', 's', or 'q'")
            else:
                result = BenchmarkResult(
                    product_id=product.id,
                    category_id=category.id,
                    score=score,
                    score_1_percent_low=score_1_percent_low,
                    test_date=test_date
                )
                db.session.add(result)
                results_added += 1
                print(f"✓ Added new result for {clean_name}: {score}" + 
                      (f" (1% low: {score_1_percent_low})" if score_1_percent_low else ""))
        
        db.session.commit()
        print(f"Import complete! Added {products_added} products and {results_added} results")
        return True

def import_csv_batch(csv_file_path, benchmark_name, benchmark_description="", unit_type="score", resolution=None, default_date=None, duplicate_action="ask"):
    """
    Import CSV with batch duplicate handling (useful for automated imports)
    
    Args:
        duplicate_action: 'ask' (default), 'update' (always update), 'skip' (always skip)
    """
    # Temporarily modify the import function for batch processing
    if duplicate_action != 'ask':
        # You can call the regular import_csv and handle duplicates programmatically
        # This is a simplified version - you'd implement the batch logic here
        pass
    
    return import_csv(csv_file_path, benchmark_name, benchmark_description, unit_type, resolution, default_date)

# Example usage script
def main():
    """
    Example of how to use the importer
    Configure your CSV files here before running
    """
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    # Import your CSV files
    csv_files = [
        # CPU productivity benchmarks (no resolution)
        {
            'file': 'photoshop_puget_suite.csv',
            'name': 'Adobe Photoshop Puget Suite',
            'description': 'Adobe Photoshop performance using Puget Systems benchmark',
            'unit': 'score',
            'resolution': None
        },
        {
            'file': 'blender_render.csv',
            'name': 'Blender Render Time',
            'description': 'Blender rendering performance benchmark',
            'unit': 'seconds',
            'resolution': None
        },
        
        # CPU gaming benchmarks (with resolution) - 3 charts per game
        {
            'file': 'starfield_cpu_1080p.csv',
            'name': 'Starfield CPU Performance',
            'description': 'Starfield CPU gaming performance',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'starfield_cpu_1440p.csv',
            'name': 'Starfield CPU Performance',
            'description': 'Starfield CPU gaming performance',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'starfield_cpu_4k.csv',
            'name': 'Starfield CPU Performance',
            'description': 'Starfield CPU gaming performance',
            'unit': 'fps',
            'resolution': '4K'
        },
        
        # GPU gaming benchmarks (with resolution) - 3 charts per game
        {
            'file': 'starfield_gpu_1080p_ultra.csv',
            'name': 'Starfield GPU Ultra',
            'description': 'Starfield GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '1080p'
        },
        {
            'file': 'starfield_gpu_1440p_ultra.csv', 
            'name': 'Starfield GPU Ultra',
            'description': 'Starfield GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '1440p'
        },
        {
            'file': 'starfield_gpu_4k_ultra.csv',
            'name': 'Starfield GPU Ultra', 
            'description': 'Starfield GPU performance at Ultra settings',
            'unit': 'fps',
            'resolution': '4K'
        },
        
        # Add more games - each game gets 6 total benchmarks:
        # 3 CPU gaming benchmarks (1080p, 1440p, 4K)
        # 3 GPU gaming benchmarks (1080p, 1440p, 4K)
        
        # Example: Cyberpunk 2077
        # {
        #     'file': 'cyberpunk_cpu_1080p.csv',
        #     'name': 'Cyberpunk 2077 CPU Performance',
        #     'description': 'Cyberpunk 2077 CPU gaming performance',
        #     'unit': 'fps',
        #     'resolution': '1080p'
        # },
        # {
        #     'file': 'cyberpunk_gpu_1080p_ultra.csv',
        #     'name': 'Cyberpunk 2077 GPU Ultra',
        #     'description': 'Cyberpunk 2077 GPU performance at Ultra settings',
        #     'unit': 'fps',
        #     'resolution': '1080p'
        # },
        # ... and so on for 1440p and 4K
    ]
    
    for csv_info in csv_files:
        print(f"\nImporting {csv_info['file']}...")
        success = import_csv(
            csv_info['file'],
            csv_info['name'],
            csv_info['description'],
            csv_info['unit'],
            csv_info.get('resolution')  # Use .get() since resolution might not be present for productivity benchmarks
        )
        if not success:
            print(f"Failed to import {csv_info['file']}")

if __name__ == '__main__':
    main()