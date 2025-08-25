import sqlite3
import re
import time
import os
from app.models import GeneratedTable
from app import db

class SQLService:
    def __init__(self, user_id):
        self.user_id = user_id
        self.db_path = f"user_dbs/user_{user_id}.db"
        self.ensure_user_db_exists()
    
    def ensure_user_db_exists(self):
        """Create user-specific database directory and file"""
        os.makedirs("user_dbs", exist_ok=True)
        
        # Create database if it doesn't exist
        if not os.path.exists(self.db_path):
            conn = sqlite3.connect(self.db_path)
            conn.close()
    
    def execute_query_with_ai_assistance(self, query, gemini_service):
        """Execute SQL query with AI assistance for table creation"""
        start_time = time.time()
        
        try:
            # First, try to execute the query directly
            result = self.execute_query(query)
            if result.get('success'):
                return result
            
            # If query failed, analyze with AI to create necessary tables
            ai_analysis = gemini_service.analyze_query_and_create_tables(query)
            
            if 'error' in ai_analysis:
                return {'error': ai_analysis['error']}
            
            # Create tables based on AI analysis
            tables_created = []
            for table_info in ai_analysis.get('tables', []):
                created = self.create_table_from_ai_analysis(table_info)
                if created:
                    tables_created.append(table_info['name'])
            
            # Try executing the original query again
            result = self.execute_query(query)
            
            if result.get('success'):
                result['ai_assisted'] = True
                result['tables_created'] = tables_created
                result['ai_explanation'] = ai_analysis.get('explanation', '')
            
            return result
            
        except Exception as e:
            return {
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def execute_query(self, query):
        """Execute SQL query on user's database"""
        start_time = time.time()
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            cursor = conn.cursor()
            
            # Execute the query
            cursor.execute(query)
            
            # Determine query type
            query_type = self.get_query_type(query)
            
            result = {
                'success': True,
                'query_type': query_type,
                'execution_time': time.time() - start_time
            }
            
            if query_type in ['SELECT']:
                # Fetch results for SELECT queries
                rows = cursor.fetchall()
                columns = [description[0] for description in cursor.description]
                
                data = []
                for row in rows:
                    data.append(dict(row))
                
                result.update({
                    'data': data,
                    'columns': columns,
                    'result_count': len(data)
                })
                
            elif query_type in ['INSERT', 'UPDATE', 'DELETE']:
                # For modification queries
                conn.commit()
                result.update({
                    'affected_rows': cursor.rowcount,
                    'result_count': cursor.rowcount
                })
                
            elif query_type in ['CREATE', 'DROP', 'ALTER']:
                # For schema modification queries
                conn.commit()
                result.update({
                    'message': f'{query_type} operation completed successfully',
                    'result_count': 1
                })
            
            conn.close()
            return result
            
        except sqlite3.Error as e:
            return {
                'error': str(e),
                'execution_time': time.time() - start_time
            }
    
    def create_table_from_ai_analysis(self, table_info):
        """Create table based on AI analysis"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Execute CREATE TABLE statement
            cursor.execute(table_info['create_statement'])
            
            # Execute INSERT statements
            for insert_stmt in table_info.get('insert_statements', []):
                cursor.execute(insert_stmt)
            
            conn.commit()
            conn.close()
            
            # Save table info to database
            generated_table = GeneratedTable(
                user_id=self.user_id,
                table_name=table_info['name'],
                table_schema=table_info.get('schema', []),
                sample_data_count=len(table_info.get('insert_statements', [])),
                created_by_ai=True
            )
            
            db.session.add(generated_table)
            db.session.commit()
            
            return True
            
        except Exception as e:
            print(f"Error creating table {table_info['name']}: {str(e)}")
            return False
    
    def get_query_type(self, query):
        """Determine the type of SQL query"""
        query = query.strip().upper()
        
        if query.startswith('SELECT'):
            return 'SELECT'
        elif query.startswith('INSERT'):
            return 'INSERT'
        elif query.startswith('UPDATE'):
            return 'UPDATE'
        elif query.startswith('DELETE'):
            return 'DELETE'
        elif query.startswith('CREATE'):
            return 'CREATE'
        elif query.startswith('DROP'):
            return 'DROP'
        elif query.startswith('ALTER'):
            return 'ALTER'
        else:
            return 'OTHER'
    
    def get_table_list(self):
        """Get list of tables in user's database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            conn.close()
            return [table[0] for table in tables]
            
        except Exception as e:
            return []
    
    def get_table_schema(self, table_name):
        """Get schema information for a specific table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            schema_info = cursor.fetchall()
            
            conn.close()
            
            schema = []
            for column in schema_info:
                schema.append({
                    'column': column[1],
                    'type': column[2],
                    'not_null': bool(column[3]),
                    'default_value': column[4],
                    'primary_key': bool(column[5])
                })
            
            return schema
            
        except Exception as e:
            return []
    
    def get_table_sample_data(self, table_name, limit=5):
        """Get sample data from a table"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
            rows = cursor.fetchall()
            
            columns = [description[0] for description in cursor.description]
            data = [dict(row) for row in rows]
            
            conn.close()
            
            return {
                'columns': columns,
                'data': data
            }
            
        except Exception as e:
            return {'error': str(e)}
