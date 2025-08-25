import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

class VisualizationService:
    def __init__(self):
        pass
    
    def create_visualization(self, data, query_type, query_text):
        """Create appropriate visualization based on query results"""
        if not data or not isinstance(data, list):
            return {'error': 'No data to visualize'}
        
        try:
            # Convert data to DataFrame for easier manipulation
            df = pd.DataFrame(data)
            
            if df.empty:
                return {'error': 'Empty dataset'}
            
            # Determine best visualization based on data characteristics
            viz_config = self.determine_visualization_type(df, query_type)
            
            if viz_config['type'] == 'table':
                return self.create_table_visualization(df)
            elif viz_config['type'] == 'bar':
                return self.create_bar_chart(df, viz_config)
            elif viz_config['type'] == 'line':
                return self.create_line_chart(df, viz_config)
            elif viz_config['type'] == 'pie':
                return self.create_pie_chart(df, viz_config)
            elif viz_config['type'] == 'scatter':
                return self.create_scatter_plot(df, viz_config)
            else:
                return self.create_table_visualization(df)
                
        except Exception as e:
            return {'error': f'Visualization error: {str(e)}'}
    
    def determine_visualization_type(self, df, query_type):
        """Determine the best visualization type based on data characteristics"""
        num_columns = len(df.columns)
        num_rows = len(df)
        
        # Get column types
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
        
        # Default configuration
        config = {
            'type': 'table',
            'x_column': None,
            'y_column': None,
            'color_column': None
        }
        
        # Simple heuristics for visualization selection
        if num_columns == 2 and len(numeric_columns) == 1 and len(categorical_columns) == 1:
            # One categorical, one numeric - bar chart
            config.update({
                'type': 'bar',
                'x_column': categorical_columns[0],
                'y_column': numeric_columns[0]
            })
        elif num_columns == 2 and len(numeric_columns) == 2:
            # Two numeric columns - scatter plot
            config.update({
                'type': 'scatter',
                'x_column': numeric_columns[0],
                'y_column': numeric_columns[1]
            })
        elif len(categorical_columns) == 1 and 'count' in [col.lower() for col in df.columns]:
            # Categorical with count - pie chart
            config.update({
                'type': 'pie',
                'labels_column': categorical_columns[0],
                'values_column': next(col for col in df.columns if 'count' in col.lower())
            })
        elif len(numeric_columns) >= 1 and any('date' in col.lower() or 'time' in col.lower() for col in df.columns):
            # Time series data - line chart
            date_col = next((col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()), None)
            if date_col:
                config.update({
                    'type': 'line',
                    'x_column': date_col,
                    'y_column': numeric_columns[0]
                })
        
        return config
    
    def create_table_visualization(self, df):
        """Create a table visualization"""
        try:
            fig = go.Figure(data=[go.Table(
                header=dict(
                    values=list(df.columns),
                    fill_color='paleturquoise',
                    align='left',
                    font=dict(size=14, color='black')
                ),
                cells=dict(
                    values=[df[col].tolist() for col in df.columns],
                    fill_color='lavender',
                    align='left',
                    font=dict(size=12, color='black')
                )
            )])
            
            fig.update_layout(
                title="Query Results",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            
            return {
                'type': 'table',
                'chart': fig.to_json(),
                'description': f'Table view of {len(df)} rows and {len(df.columns)} columns'
            }
            
        except Exception as e:
            return {'error': f'Table visualization error: {str(e)}'}
    
    def create_bar_chart(self, df, config):
        """Create a bar chart visualization"""
        try:
            x_col = config['x_column']
            y_col = config['y_column']
            
            fig = px.bar(
                df, 
                x=x_col, 
                y=y_col,
                title=f'{y_col} by {x_col}',
                color=y_col,
                color_continuous_scale='viridis'
            )
            
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col,
                showlegend=False
            )
            
            return {
                'type': 'bar',
                'chart': fig.to_json(),
                'description': f'Bar chart showing {y_col} distribution across {x_col}'
            }
            
        except Exception as e:
            return {'error': f'Bar chart error: {str(e)}'}
    
    def create_line_chart(self, df, config):
        """Create a line chart visualization"""
        try:
            x_col = config['x_column']
            y_col = config['y_column']
            
            fig = px.line(
                df, 
                x=x_col, 
                y=y_col,
                title=f'{y_col} over {x_col}',
                markers=True
            )
            
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col
            )
            
            return {
                'type': 'line',
                'chart': fig.to_json(),
                'description': f'Line chart showing {y_col} trend over {x_col}'
            }
            
        except Exception as e:
            return {'error': f'Line chart error: {str(e)}'}
    
    def create_pie_chart(self, df, config):
        """Create a pie chart visualization"""
        try:
            labels_col = config['labels_column']
            values_col = config['values_column']
            
            fig = px.pie(
                df,
                values=values_col,
                names=labels_col,
                title=f'Distribution of {values_col} by {labels_col}'
            )
            
            return {
                'type': 'pie',
                'chart': fig.to_json(),
                'description': f'Pie chart showing distribution of {values_col} across {labels_col}'
            }
            
        except Exception as e:
            return {'error': f'Pie chart error: {str(e)}'}
    
    def create_scatter_plot(self, df, config):
        """Create a scatter plot visualization"""
        try:
            x_col = config['x_column']
            y_col = config['y_column']
            
            fig = px.scatter(
                df,
                x=x_col,
                y=y_col,
                title=f'{y_col} vs {x_col}',
                color=y_col,
                size=y_col,
                hover_data=df.columns.tolist()
            )
            
            fig.update_layout(
                xaxis_title=x_col,
                yaxis_title=y_col
            )
            
            return {
                'type': 'scatter',
                'chart': fig.to_json(),
                'description': f'Scatter plot showing relationship between {x_col} and {y_col}'
            }
            
        except Exception as e:
            return {'error': f'Scatter plot error: {str(e)}'}
    
    def create_query_flow_diagram(self, query_text, query_type):
        """Create a visual representation of SQL query execution flow"""
        try:
            # This is a simplified implementation
            # In a real application, you might want to use a more sophisticated SQL parser
            
            steps = []
            
            if query_type == 'SELECT':
                steps = self.parse_select_query(query_text)
            elif query_type == 'INSERT':
                steps = self.parse_insert_query(query_text)
            elif query_type == 'UPDATE':
                steps = self.parse_update_query(query_text)
            elif query_type == 'DELETE':
                steps = self.parse_delete_query(query_text)
            
            # Create a simple flowchart
            fig = go.Figure()
            
            # Add nodes for each step
            for i, step in enumerate(steps):
                fig.add_trace(go.Scatter(
                    x=[i],
                    y=[0],
                    mode='markers+text',
                    marker=dict(size=80, color='lightblue'),
                    text=[step],
                    textposition='middle center',
                    name=f'Step {i+1}'
                ))
                
                # Add arrows between steps
                if i < len(steps) - 1:
                    fig.add_annotation(
                        x=i+0.4, y=0,
                        ax=i+0.6, ay=0,
                        arrowhead=2, arrowsize=1, arrowwidth=2, arrowcolor='black'
                    )
            
            fig.update_layout(
                title=f'SQL {query_type} Query Execution Flow',
                showlegend=False,
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                height=200
            )
            
            return {
                'type': 'flow',
                'chart': fig.to_json(),
                'description': f'Execution flow for {query_type} query'
            }
            
        except Exception as e:
            return {'error': f'Flow diagram error: {str(e)}'}
    
    def parse_select_query(self, query):
        """Parse SELECT query to identify execution steps"""
        steps = ['FROM Tables', 'WHERE Filter', 'GROUP BY', 'HAVING', 'SELECT Columns', 'ORDER BY']
        
        # Simplified parsing - check which clauses are present
        present_steps = []
        query_upper = query.upper()
        
        if 'FROM' in query_upper:
            present_steps.append('FROM Tables')
        if 'WHERE' in query_upper:
            present_steps.append('WHERE Filter')
        if 'GROUP BY' in query_upper:
            present_steps.append('GROUP BY')
        if 'HAVING' in query_upper:
            present_steps.append('HAVING')
        if 'SELECT' in query_upper:
            present_steps.append('SELECT Columns')
        if 'ORDER BY' in query_upper:
            present_steps.append('ORDER BY')
        
        return present_steps if present_steps else ['SELECT']
    
    def parse_insert_query(self, query):
        """Parse INSERT query to identify execution steps"""
        return ['Prepare Data', 'Validate Constraints', 'INSERT Records']
    
    def parse_update_query(self, query):
        """Parse UPDATE query to identify execution steps"""
        return ['Find Records', 'Apply WHERE Filter', 'UPDATE Values', 'Validate Constraints']
    
    def parse_delete_query(self, query):
        """Parse DELETE query to identify execution steps"""
        return ['Find Records', 'Apply WHERE Filter', 'DELETE Records']
