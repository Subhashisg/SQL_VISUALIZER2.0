from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import SQLQuery, GeneratedTable
from app.services.gemini_service import GeminiService
from app.services.sql_service import SQLService
from app import db
import json

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent queries
    recent_queries = SQLQuery.query.filter_by(user_id=current_user.id)\
                                 .order_by(SQLQuery.created_at.desc())\
                                 .limit(10).all()
    
    # Get user's generated tables
    generated_tables = GeneratedTable.query.filter_by(user_id=current_user.id)\
                                          .order_by(GeneratedTable.created_at.desc())\
                                          .all()
    
    # Check if user has API key
    has_api_key = current_user.get_gemini_api_key() is not None
    
    return render_template('dashboard.html', 
                         recent_queries=recent_queries,
                         generated_tables=generated_tables,
                         has_api_key=has_api_key)

@main_bp.route('/sql-playground')
@login_required
def sql_playground():
    # Check if user has API key
    if not current_user.get_gemini_api_key():
        return render_template('no_api_key.html')
    
    # Get user's tables
    generated_tables = GeneratedTable.query.filter_by(user_id=current_user.id).all()
    
    return render_template('sql_playground.html', tables=generated_tables)

@main_bp.route('/execute-sql', methods=['POST'])
@login_required
def execute_sql():
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        api_key = current_user.get_gemini_api_key()
        if not api_key:
            return jsonify({'error': 'Gemini API key not configured'}), 400
        
        # Initialize services
        gemini_service = GeminiService(api_key)
        sql_service = SQLService(current_user.id)
        
        # Check if query requires table creation
        result = sql_service.execute_query_with_ai_assistance(query, gemini_service)
        
        # Log the query
        sql_query = SQLQuery(
            user_id=current_user.id,
            query_text=query,
            query_type=result.get('query_type', 'UNKNOWN'),
            execution_time=result.get('execution_time', 0),
            result_count=result.get('result_count', 0),
            result_data=result.get('data', []),
            error_message=result.get('error')
        )
        
        db.session.add(sql_query)
        db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/get-query-visualization/<int:query_id>')
@login_required
def get_query_visualization(query_id):
    try:
        query = SQLQuery.query.filter_by(id=query_id, user_id=current_user.id).first()
        if not query:
            return jsonify({'error': 'Query not found'}), 404
        
        # Generate visualization based on query type and results
        from app.services.visualization_service import VisualizationService
        viz_service = VisualizationService()
        
        visualization = viz_service.create_visualization(
            query.result_data,
            query.query_type,
            query.query_text
        )
        
        return jsonify(visualization)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/learning-materials')
@login_required
def learning_materials():
    return render_template('learning_materials.html')

@main_bp.route('/query-history')
@login_required
def query_history():
    page = request.args.get('page', 1, type=int)
    queries = SQLQuery.query.filter_by(user_id=current_user.id)\
                           .order_by(SQLQuery.created_at.desc())\
                           .paginate(page=page, per_page=20, error_out=False)
    
    return render_template('query_history.html', queries=queries)
