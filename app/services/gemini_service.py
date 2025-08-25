from google import genai
from google.genai import types
import json
import re

class GeminiService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = genai.Client(api_key=api_key)
    
    def test_connection(self):
        """Test if the API key is valid"""
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Hello, this is a test."
            )
            return {'success': True, 'message': 'API key is valid'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def analyze_query_and_create_tables(self, query):
        """Analyze SQL query and create necessary tables with sample data"""
        try:
            system_instruction = """
            You are a SQL expert and database assistant. Analyze the provided SQL query and:
            
            1. Identify all table names referenced in the query
            2. For each table, generate a realistic schema with appropriate column names and data types
            3. Provide CREATE TABLE statements
            4. Generate INSERT statements with realistic sample data (at least 10 rows per table)
            5. Ensure the data is diverse and realistic for the context
            
            Return your response as a JSON object with this structure:
            {
                "tables": [
                    {
                        "name": "table_name",
                        "create_statement": "CREATE TABLE ...",
                        "schema": [
                            {"column": "id", "type": "INTEGER", "constraints": "PRIMARY KEY"},
                            {"column": "name", "type": "VARCHAR(100)", "constraints": "NOT NULL"}
                        ],
                        "insert_statements": ["INSERT INTO table_name ...", ...]
                    }
                ],
                "explanation": "Brief explanation of the tables created and their purpose"
            }
            
            Make the data contextually appropriate. For example:
            - If querying employees, create realistic employee data
            - If querying products, create realistic product data
            - Use appropriate constraints and relationships
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
                contents=f"Analyze this SQL query and create necessary tables: {query}"
            )
            
            # Extract JSON from response
            response_text = response.text
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {'error': 'Could not parse response from AI'}
                
        except Exception as e:
            return {'error': f'Error analyzing query: {str(e)}'}
    
    def explain_sql_query(self, query):
        """Provide detailed explanation of SQL query"""
        try:
            system_instruction = """
            You are a SQL tutor. Explain the provided SQL query in a clear, educational manner using Markdown formatting.
            Include:
            1. What the query does (purpose)
            2. Step-by-step breakdown of each clause
            3. Key concepts and keywords used
            4. Expected output format
            5. Any best practices or potential improvements
            
            Format your response using Markdown:
            - Use ## for major sections
            - Use backticks for SQL code and keywords
            - Use bullet points for lists
            - Use bold and italic for emphasis
            - Use code blocks for example queries
            
            Make it beginner-friendly but comprehensive.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
                contents=f"Explain this SQL query in markdown format: {query}"
            )
            
            return {'explanation': response.text, 'format': 'markdown'}
            
        except Exception as e:
            return {'error': f'Error explaining query: {str(e)}'}
    
    def suggest_query_improvements(self, query):
        """Suggest improvements for SQL query"""
        try:
            system_instruction = """
            You are a database optimization expert. Analyze the provided SQL query and suggest improvements using Markdown formatting.
            Focus on:
            1. Performance optimizations
            2. Best practices
            3. Code readability
            4. Security considerations
            5. Alternative approaches
            
            Format your response using Markdown:
            - Use ## for major sections
            - Use backticks for SQL code and keywords
            - Use bullet points for lists
            - Use bold and italic for emphasis
            - Use code blocks for example queries
            - Use tables when comparing options
            
            Provide specific suggestions with explanations.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
                contents=f"Suggest improvements for this SQL query in markdown format: {query}"
            )
            
            return {'suggestions': response.text, 'format': 'markdown'}
            
        except Exception as e:
            return {'error': f'Error generating suggestions: {str(e)}'}
    
    def generate_sample_data(self, table_schema, row_count=10):
        """Generate sample data for a table schema"""
        try:
            system_instruction = f"""
            Generate {row_count} rows of realistic sample data for a table with the following schema:
            {json.dumps(table_schema, indent=2)}
            
            Return INSERT statements that would populate this table with diverse, realistic data.
            Ensure data consistency and relationships where applicable.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
                contents="Generate the sample data INSERT statements"
            )
            
            return {'insert_statements': response.text}
            
        except Exception as e:
            return {'error': f'Error generating sample data: {str(e)}'}
    
    def generate_learning_content(self, topic):
        """Generate educational content for SQL topics"""
        try:
            system_instruction = """
            You are a SQL educator. Create comprehensive learning content for the requested SQL topic using Markdown formatting.
            Include:
            1. Clear explanation of the concept
            2. Syntax and examples
            3. Common use cases
            4. Best practices
            5. Common mistakes to avoid
            6. Practice exercises
            
            Format your response using Markdown:
            - Use # for the main title
            - Use ## for major sections
            - Use ### for subsections
            - Use backticks for SQL code and keywords
            - Use bullet points for lists
            - Use bold and italic for emphasis
            - Use code blocks for example queries
            - Use tables for comparing concepts
            - Use > for important notes or tips
            
            Make it structured and easy to follow.
            """
            
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
                contents=f"Create learning content for SQL topic: {topic} in markdown format"
            )
            
            return {'content': response.text, 'format': 'markdown'}
            
        except Exception as e:
            return {'error': f'Error generating learning content: {str(e)}'}
