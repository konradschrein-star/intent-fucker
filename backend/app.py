"""
Flask Backend for Keyword Classifier
Provides REST API for the frontend
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import uuid
import threading
from pathlib import Path
from datetime import datetime

from ollama_client import OllamaClient
from classifier import KeywordClassifier
from csv_processor import CSVProcessor
from config import (
    DEFAULT_CONFIDENCE_THRESHOLD,
    DEFAULT_CATEGORIES,
    DEFAULT_RELEVANCE_PROMPT,
    DEFAULT_CATEGORY_PROMPT,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_MB
)

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = Path('../uploads')
OUTPUT_FOLDER = Path('../outputs')
UPLOAD_FOLDER.mkdir(exist_ok=True)
OUTPUT_FOLDER.mkdir(exist_ok=True)

# Global state
ollama_client = OllamaClient()
jobs = {}  # Store job status and results


class ProcessingJob:
    def __init__(self, job_id, topic, keywords):
        self.job_id = job_id
        self.topic = topic
        self.keywords = keywords
        self.status = 'pending'  # pending, processing, completed, failed
        self.progress = 0
        self.total = len(keywords)
        self.current_keyword = ''
        self.results = []
        self.error = None
        self.accepted_file = None
        self.rejected_file = None
        self.statistics = {}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if Ollama is available"""
    ollama_available = ollama_client.is_available()
    models = ollama_client.list_models() if ollama_available else []
    
    return jsonify({
        'status': 'ok',
        'ollama_available': ollama_available,
        'models': models
    })


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and validate CSV file"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400
    
    try:
        # Save file
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = UPLOAD_FOLDER / filename
        file.save(filepath)
        
        # Validate CSV
        processor = CSVProcessor()
        success, message, df = processor.load_csv(str(filepath))
        
        if not success:
            os.remove(filepath)
            return jsonify({'error': message}), 400
        
        return jsonify({
            'success': True,
            'filename': filename,
            'filepath': str(filepath),
            'keyword_count': len(df),
            'message': message
        })
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500


@app.route('/api/settings', methods=['GET'])
def get_settings():
    """Get current settings"""
    return jsonify({
        'confidence_threshold': DEFAULT_CONFIDENCE_THRESHOLD,
        'categories': DEFAULT_CATEGORIES,
        'relevance_prompt': DEFAULT_RELEVANCE_PROMPT,
        'category_prompt': DEFAULT_CATEGORY_PROMPT
    })


@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update settings (categories, prompts, threshold)"""
    # This endpoint allows updating settings for future processing
    # For now, we return success - settings will be passed per-job
    return jsonify({'success': True})


@app.route('/api/process', methods=['POST'])
def start_processing():
    """Start keyword classification job"""
    data = request.json
    
    # Extract parameters
    topic = data.get('topic', '')
    confidence_threshold = data.get('confidence_threshold', DEFAULT_CONFIDENCE_THRESHOLD)
    categories = data.get('categories', DEFAULT_CATEGORIES)
    relevance_prompt = data.get('relevance_prompt', DEFAULT_RELEVANCE_PROMPT)
    category_prompt = data.get('category_prompt', DEFAULT_CATEGORY_PROMPT)
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    # Load keywords
    processor = CSVProcessor()
    
    if 'filepath' in data:
        # Load from uploaded file
        success, message, df = processor.load_csv(data['filepath'])
        if not success:
            return jsonify({'error': message}), 400
    elif 'manual_input' in data:
        # Parse manual input
        processor.parse_manual_input(data['manual_input'])
    else:
        return jsonify({'error': 'No keywords provided'}), 400
    
    keywords = processor.get_keywords()
    
    if not keywords:
        return jsonify({'error': 'No keywords to process'}), 400
    
    # Create job
    job_id = str(uuid.uuid4())
    job = ProcessingJob(job_id, topic, keywords)
    jobs[job_id] = job
    
    # Start processing in background thread
    thread = threading.Thread(
        target=process_keywords,
        args=(job_id, topic, keywords, confidence_threshold, categories, relevance_prompt, category_prompt)
    )
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'success': True,
        'job_id': job_id,
        'total_keywords': len(keywords)
    })


def process_keywords(job_id, topic, keywords, confidence_threshold, categories, relevance_prompt, category_prompt):
    """Background processing of keywords"""
    job = jobs[job_id]
    job.status = 'processing'
    
    try:
        # Initialize classifier
        classifier = KeywordClassifier(ollama_client)
        classifier.set_confidence_threshold(confidence_threshold)
        classifier.categories = categories
        classifier.set_relevance_prompt(relevance_prompt)
        classifier.set_category_prompt(category_prompt)
        
        # Initialize processor
        processor = CSVProcessor()
        
        # Process each keyword
        for idx, keyword_data in enumerate(keywords):
            keyword = keyword_data['title']
            job.current_keyword = keyword
            
            # Classify keyword
            result = classifier.classify_keyword(keyword, topic)
            
            # Add to processor results
            processor.add_result(keyword_data, result)
            
            # Update progress
            job.progress = idx + 1
        
        # Export results
        accepted_file, rejected_file = processor.export_results(str(OUTPUT_FOLDER))
        job.accepted_file = accepted_file
        job.rejected_file = rejected_file
        
        # Get statistics
        job.statistics = processor.get_statistics()
        
        # Mark as completed
        job.status = 'completed'
        
    except Exception as e:
        job.status = 'failed'
        job.error = str(e)
        print(f"Error processing job {job_id}: {e}")


@app.route('/api/progress/<job_id>', methods=['GET'])
def get_progress(job_id):
    """Get job progress"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    
    return jsonify({
        'status': job.status,
        'progress': job.progress,
        'total': job.total,
        'current_keyword': job.current_keyword,
        'percentage': round((job.progress / job.total * 100), 2) if job.total > 0 else 0
    })


@app.route('/api/results/<job_id>', methods=['GET'])
def get_results(job_id):
    """Get job results"""
    if job_id not in jobs:
        return jsonify({'error': 'Job not found'}), 404
    
    job = jobs[job_id]
    
    if job.status != 'completed':
        return jsonify({'error': 'Job not completed yet'}), 400
    
    return jsonify({
        'status': 'completed',
        'statistics': job.statistics,
        'accepted_file': job.accepted_file,
        'rejected_file': job.rejected_file
    })


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download result CSV file"""
    filepath = OUTPUT_FOLDER / filename
    
    if not filepath.exists():
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 Keyword Classifier Backend Starting...")
    print("=" * 60)
    
    # Check Ollama status
    if ollama_client.is_available():
        print("✅ Ollama is running")
        models = ollama_client.list_models()
        print(f"📦 Available models: {', '.join(models)}")
    else:
        print("⚠️  WARNING: Ollama is not running!")
        print("   Please start Ollama service before processing keywords")
    
    print("\n🌐 Starting Flask server on http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
