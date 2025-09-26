# models.py
# Complete Flask database setup for CPU/GPU benchmark comparison website
# Supports both productivity benchmarks (no resolution) and gaming benchmarks (with resolution)
# CPU gaming benchmarks: FPS at different resolutions (1080p, 1440p, 4K)
# GPU gaming benchmarks: FPS + 1% low at different resolutions (1080p, 1440p, 4K)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///benchmarks.db'  # Use PostgreSQL in production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(10), nullable=False)  # 'CPU' or 'GPU'
    core_count = db.Column(db.String(20))  # e.g., "(8C/16T)" or "(8P/16E/32T)"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to benchmark results
    benchmark_results = db.relationship('BenchmarkResult', backref='product', lazy=True)
    
    def __repr__(self):
        return f'<Product {self.name}>'

class BenchmarkCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(200))
    unit_type = db.Column(db.String(20))  # 'score', 'fps', 'seconds', etc.
    product_type = db.Column(db.String(10), nullable=False)  # 'CPU' or 'GPU'
    resolution = db.Column(db.String(10), nullable=True)  # '1080p', '1440p', '4K' (gaming benchmarks only)
    
    # Relationship to benchmark results
    benchmark_results = db.relationship('BenchmarkResult', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<BenchmarkCategory {self.name}>'

class BenchmarkResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('benchmark_category.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)  # Main score (avg fps for gaming, score for productivity)
    score_1_percent_low = db.Column(db.Float, nullable=True)  # 1% low fps (GPU gaming only)
    test_date = db.Column(db.String(10))  # e.g., "[7/24]"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Ensure unique combination of product + category
    __table_args__ = (db.UniqueConstraint('product_id', 'category_id', name='unique_product_category'),)
    
    def __repr__(self):
        return f'<BenchmarkResult {self.product.name}: {self.score}>'

# Initialize database
def create_tables():
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    create_tables()


# csv_importer.py
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

def import_csv(csv_file_path, benchmark_name, benchmark_description="", unit_type="score", resolution=None):
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
        
        # Check for GPU format columns
        gpu_columns = ['GPU_Model', 'Date', 'AVG_FPS', '1%_Low']
        if all(col in df.columns for col in gpu_columns):
            is_gpu_format = True
            product_col = 'GPU_Model'
            score_col = 'AVG_FPS'
            core_count_col = None
            print("Detected GPU CSV format")
        else:
            # Check for CPU format columns
            cpu_columns = ['CPU_Model', 'Core_Count', 'Date', 'Score']
            if not all(col in df.columns for col in cpu_columns):
                print(f"CSV must have either GPU columns {gpu_columns} or CPU columns {cpu_columns}")
                return False
            product_col = 'CPU_Model'
            score_col = 'Score'
            core_count_col = 'Core_Count'
            print("Detected CPU CSV format")
        
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
                existing_result.score = score
                existing_result.score_1_percent_low = score_1_percent_low
                existing_result.test_date = test_date
                print(f"Updated result for {clean_name}: {score}" + 
                      (f" (1% low: {score_1_percent_low})" if score_1_percent_low else ""))
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
        
        db.session.commit()
        print(f"Import complete! Added {products_added} products and {results_added} results")
        return True

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