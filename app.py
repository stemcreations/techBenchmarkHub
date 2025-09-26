# app.py
# Main Flask application entry point
from flask import Flask, render_template, jsonify, request
from models import app, db, create_tables

# Import your routes here when you create them
# from routes import *

@app.route('/')
def index():
    """Main dashboard page"""
    return "Tech Benchmark Hub - Coming Soon!"

@app.route('/api/status')
def api_status():
    """API health check"""
    return jsonify({
        'status': 'ok',
        'message': 'Tech Benchmark Hub API is running'
    })

if __name__ == '__main__':
    # Initialize database tables
    create_tables()
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)