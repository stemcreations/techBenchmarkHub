# app.py
# Main Flask application entry point
from flask import Flask, render_template, jsonify, request
from models import app, db, create_tables, Product, BenchmarkCategory, BenchmarkResult
from sqlalchemy import func

# Import your routes here when you create them
# from routes import *

@app.route('/')
def index():
    """Main dashboard page"""
    # Check if this is an API request (AJAX)
    if request.headers.get('Content-Type') == 'application/json' or request.args.get('api'):
        # Return JSON data for AJAX requests
        total_products = Product.query.count()
        total_benchmarks = BenchmarkCategory.query.count()
        total_results = BenchmarkResult.query.count()
        
        cpu_count = Product.query.filter_by(type='CPU').count()
        gpu_count = Product.query.filter_by(type='GPU').count()
        
        stats = {
            'total_products': total_products,
            'total_benchmarks': total_benchmarks,
            'total_results': total_results,
            'cpu_count': cpu_count,
            'gpu_count': gpu_count
        }
        
        return jsonify({
            'message': 'Welcome to Tech Benchmark Hub!',
            'stats': stats
        })
    else:
        # Return HTML template for browser requests
        return render_template('index.html')

@app.route('/api/stats')
def api_stats():
    """Get database statistics"""
    total_products = Product.query.count()
    total_benchmarks = BenchmarkCategory.query.count()
    total_results = BenchmarkResult.query.count()
    
    cpu_count = Product.query.filter_by(type='CPU').count()
    gpu_count = Product.query.filter_by(type='GPU').count()
    
    stats = {
        'total_products': total_products,
        'total_benchmarks': total_benchmarks,
        'total_results': total_results,
        'cpu_count': cpu_count,
        'gpu_count': gpu_count
    }
    
    return jsonify({
        'message': 'Welcome to Tech Benchmark Hub!',
        'stats': stats
    })

@app.route('/api/status')
def api_status():
    """API health check"""
    return jsonify({
        'status': 'ok',
        'message': 'Tech Benchmark Hub API is running'
    })

@app.route('/api/products')
def get_products():
    """Get all products with optional filtering"""
    product_type = request.args.get('type')  # 'CPU' or 'GPU'
    
    query = Product.query
    if product_type:
        query = query.filter_by(type=product_type.upper())
    
    products = query.all()
    
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'type': p.type,
        'core_count': p.core_count,
        'benchmark_count': len(p.benchmark_results)
    } for p in products])

@app.route('/api/benchmarks')
def get_benchmarks():
    """Get all benchmark categories"""
    product_type = request.args.get('type')  # Filter by CPU or GPU
    
    query = BenchmarkCategory.query
    if product_type:
        query = query.filter_by(product_type=product_type.upper())
    
    benchmarks = query.all()
    
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'description': b.description,
        'unit_type': b.unit_type,
        'product_type': b.product_type,
        'resolution': b.resolution,
        'result_count': len(b.benchmark_results)
    } for b in benchmarks])

@app.route('/api/benchmark/<int:benchmark_id>/results')
def get_benchmark_results(benchmark_id):
    """Get results for a specific benchmark, sorted by score"""
    benchmark = BenchmarkCategory.query.get_or_404(benchmark_id)
    
    results = BenchmarkResult.query\
        .filter_by(category_id=benchmark_id)\
        .join(Product)\
        .order_by(BenchmarkResult.score.desc())\
        .all()
    
    return jsonify({
        'benchmark': {
            'id': benchmark.id,
            'name': benchmark.name,
            'description': benchmark.description,
            'unit_type': benchmark.unit_type,
            'product_type': benchmark.product_type,
            'resolution': benchmark.resolution
        },
        'results': [{
            'product_name': r.product.name,
            'product_type': r.product.type,
            'core_count': r.product.core_count,
            'score': r.score,
            'score_1_percent_low': r.score_1_percent_low,
            'test_date': r.test_date
        } for r in results]
    })

@app.route('/api/product/<int:product_id>/results')
def get_product_results(product_id):
    """Get all benchmark results for a specific product"""
    product = Product.query.get_or_404(product_id)
    
    results = BenchmarkResult.query\
        .filter_by(product_id=product_id)\
        .join(BenchmarkCategory)\
        .order_by(BenchmarkCategory.name)\
        .all()
    
    return jsonify({
        'product': {
            'id': product.id,
            'name': product.name,
            'type': product.type,
            'core_count': product.core_count
        },
        'results': [{
            'benchmark_name': r.category.name,
            'benchmark_description': r.category.description,
            'unit_type': r.category.unit_type,
            'resolution': r.category.resolution,
            'score': r.score,
            'score_1_percent_low': r.score_1_percent_low,
            'test_date': r.test_date
        } for r in results]
    })

@app.route('/api/top-performers')
def get_top_performers():
    """Get top performing products across different categories"""
    # Get top CPU for Photoshop
    photoshop_winner = db.session.query(BenchmarkResult, Product)\
        .join(Product)\
        .join(BenchmarkCategory)\
        .filter(BenchmarkCategory.name == 'Adobe Photoshop Puget Suite')\
        .order_by(BenchmarkResult.score.desc())\
        .first()
    
    # Get top CPU for gaming (using Baldur's Gate 3 as example)
    gaming_cpu_winner = db.session.query(BenchmarkResult, Product)\
        .join(Product)\
        .join(BenchmarkCategory)\
        .filter(BenchmarkCategory.name.like("Baldur's Gate 3 CPU Performance%"))\
        .order_by(BenchmarkResult.score.desc())\
        .first()
    
    # Get top GPU for 1080p gaming (using Cyberpunk as example)
    gaming_gpu_winner = db.session.query(BenchmarkResult, Product)\
        .join(Product)\
        .join(BenchmarkCategory)\
        .filter(BenchmarkCategory.name == 'Cyberpunk 2077 Ultra 1080p')\
        .order_by(BenchmarkResult.score.desc())\
        .first()
    
    top_performers = {}
    
    if photoshop_winner:
        top_performers['photoshop_cpu'] = {
            'product': photoshop_winner[1].name,
            'score': photoshop_winner[0].score,
            'benchmark': 'Adobe Photoshop Puget Suite'
        }
    
    if gaming_cpu_winner:
        top_performers['gaming_cpu'] = {
            'product': gaming_cpu_winner[1].name,
            'score': gaming_cpu_winner[0].score,
            'benchmark': "Baldur's Gate 3 CPU Performance"
        }
    
    if gaming_gpu_winner:
        top_performers['gaming_gpu_1080p'] = {
            'product': gaming_gpu_winner[1].name,
            'score': gaming_gpu_winner[0].score,
            'score_1_percent_low': gaming_gpu_winner[0].score_1_percent_low,
            'benchmark': 'Cyberpunk 2077 Ultra 1080p'
        }
    
    return jsonify(top_performers)

if __name__ == '__main__':
    # Initialize database tables
    create_tables()
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)