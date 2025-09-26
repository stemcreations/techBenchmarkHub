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