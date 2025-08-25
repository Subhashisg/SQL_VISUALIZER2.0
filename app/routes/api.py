from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import GeneratedTable
from app.services.gemini_service import GeminiService
from app import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/test-api-key', methods=['POST'])
@login_required
def test_api_key():
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
        
        # Test the API key with a simple request
        gemini_service = GeminiService(api_key)
        test_result = gemini_service.test_connection()
        
        if test_result['success']:
            return jsonify({'success': True, 'message': 'API key is valid'})
        else:
            return jsonify({'error': test_result['error']}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/generate-sample-data', methods=['POST'])
@login_required
def generate_sample_data():
    try:
        data = request.get_json()
        table_name = data.get('table_name')
        row_count = data.get('row_count', 10)
        
        if not table_name:
            return jsonify({'error': 'Table name is required'}), 400
        
        api_key = current_user.get_gemini_api_key()
        if not api_key:
            return jsonify({'error': 'Gemini API key not configured'}), 400
        
        # Check if table exists
        table = GeneratedTable.query.filter_by(
            user_id=current_user.id,
            table_name=table_name
        ).first()
        
        if not table:
            return jsonify({'error': 'Table not found'}), 404
        
        gemini_service = GeminiService(api_key)
        result = gemini_service.generate_sample_data(table.table_schema, row_count)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/explain-query', methods=['POST'])
@login_required
def explain_query():
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        api_key = current_user.get_gemini_api_key()
        if not api_key:
            return jsonify({'error': 'Gemini API key not configured'}), 400
        
        gemini_service = GeminiService(api_key)
        explanation = gemini_service.explain_sql_query(query)
        
        return jsonify(explanation)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/suggest-improvements', methods=['POST'])
@login_required
def suggest_improvements():
    try:
        data = request.get_json()
        query = data.get('query')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        api_key = current_user.get_gemini_api_key()
        if not api_key:
            return jsonify({'error': 'Gemini API key not configured'}), 400
        
        gemini_service = GeminiService(api_key)
        suggestions = gemini_service.suggest_query_improvements(query)
        
        return jsonify(suggestions)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/get-table-info/<table_name>')
@login_required
def get_table_info(table_name):
    try:
        table = GeneratedTable.query.filter_by(
            user_id=current_user.id,
            table_name=table_name
        ).first()
        
        if not table:
            return jsonify({'error': 'Table not found'}), 404
        
        return jsonify({
            'table_name': table.table_name,
            'schema': table.table_schema,
            'sample_data_count': table.sample_data_count,
            'created_at': table.created_at.isoformat(),
            'created_by_ai': table.created_by_ai
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
