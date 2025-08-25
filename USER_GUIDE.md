# 🚀 SQL Visualizer - AI-Powered SQL Learning Platform

A comprehensive Flask-based web application that helps users learn SQL interactively with Google Gemini AI assistance.

## ✨ Features

### 🔐 **User Management & Security**
- **Secure User Authentication**: Registration/login system with password hashing
- **Encrypted API Key Storage**: Google Gemini API keys are encrypted using Fernet encryption
- **Personal Database Isolation**: Each user gets their own SQLite database environment
- **Session Management**: Secure session handling with Flask-Login

### 🤖 **AI-Powered Learning**
- **Automatic Table Generation**: AI creates tables and sample data based on your SQL queries
- **Query Explanation**: Get detailed explanations of how your SQL queries work
- **Query Optimization Suggestions**: AI provides tips to improve your SQL performance
- **Interactive Learning Path**: Structured learning materials from beginner to advanced

### 📊 **Data Visualization**
- **Multiple Chart Types**: Bar charts, line charts, pie charts, scatter plots
- **Interactive Tables**: Searchable and sortable result tables
- **Query Flow Diagrams**: Visual representation of SQL query execution steps
- **Real-time Results**: Instant query execution and visualization

### 💾 **Query Management**
- **History Tracking**: Keep track of all your queries and results
- **Performance Metrics**: Execution time and result count tracking
- **Export Functionality**: Export your query history and results
- **Query Templates**: Pre-built examples for common SQL patterns

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key (get from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Quick Start

1. **Clone or download the project**
   ```bash
   # Navigate to the project directory
   cd sql_visualiser
   ```

2. **Run the setup script**
   ```bash
   # On Windows
   setup_and_run.bat
   
   # Or manually:
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   python run.py
   ```

3. **Open your browser**
   - Go to http://localhost:5000
   - Register a new account
   - Add your Gemini API key in settings

## 📋 Usage Guide

### 1. **First Time Setup**
1. Register an account with username, email, and password
2. Log in to your account
3. Go to Settings and add your Google Gemini API key
4. Test the API key connection

### 2. **Writing SQL Queries**
1. Navigate to **SQL Playground**
2. Write any SQL query in the editor (syntax highlighting included)
3. Click **Execute** - AI will create tables automatically if they don't exist
4. View results in table format or interactive charts

### 3. **Learning SQL**
1. Visit **Learning Materials** for structured lessons
2. Try **Quick Examples** in the playground
3. Use **Explain** button to understand queries
4. Get **Improvement Suggestions** from AI

### 4. **Managing Your Work**
1. View all queries in **Query History**
2. Re-run previous queries
3. Export your learning progress
4. Track performance improvements

## 🎯 Example Queries

The AI can automatically create tables for queries like:

```sql
-- Employee Management
SELECT name, department, salary 
FROM employees 
WHERE salary > 50000 
ORDER BY salary DESC;

-- Sales Analysis
SELECT product_name, SUM(quantity) as total_sold
FROM sales s
JOIN products p ON s.product_id = p.id
WHERE sale_date >= '2024-01-01'
GROUP BY product_name;

-- Customer Insights
SELECT c.name, COUNT(o.id) as order_count
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.name
HAVING COUNT(o.id) > 5;
```

## 🏗️ Technical Architecture

### Backend
- **Flask**: Web framework with Blueprint organization
- **SQLAlchemy**: ORM for database operations
- **Flask-Login**: User session management
- **Cryptography**: API key encryption
- **Google Genai**: AI integration

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **CodeMirror**: SQL syntax highlighting
- **Plotly.js**: Interactive data visualizations
- **Font Awesome**: Icons and visual elements

### Database Structure
- **Users**: User accounts and authentication
- **APIKeys**: Encrypted API key storage
- **SQLQueries**: Query history and results
- **GeneratedTables**: AI-created table metadata

## 🔧 Configuration

### Environment Variables (.env)
```bash
SECRET_KEY=your-flask-secret-key
DATABASE_URL=sqlite:///sql_visualizer.db
ENCRYPTION_KEY=your-fernet-encryption-key
FLASK_ENV=development
```

### File Structure
```
sql_visualiser/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── routes/              # Route blueprints
│   │   ├── auth.py         # Authentication routes
│   │   ├── main.py         # Main application routes
│   │   └── api.py          # API endpoints
│   ├── services/            # Business logic
│   │   ├── gemini_service.py    # AI integration
│   │   ├── sql_service.py       # SQL execution
│   │   └── visualization_service.py # Charts & graphs
│   ├── templates/           # HTML templates
│   └── static/             # CSS, JS, images
├── requirements.txt        # Python dependencies
├── run.py                 # Application entry point
├── setup_and_run.bat     # Windows setup script
└── .env                  # Environment configuration
```

## 🚨 Security Features

1. **Password Hashing**: Using Werkzeug's secure password hashing
2. **API Key Encryption**: Fernet symmetric encryption for API keys
3. **SQL Injection Protection**: Parameterized queries and ORM usage
4. **User Isolation**: Separate database environments per user
5. **CSRF Protection**: Flask-WTF CSRF tokens
6. **Session Security**: Secure cookie settings

## 🎓 Learning Path

### Beginner
- Basic SELECT statements
- WHERE clauses and filtering
- ORDER BY and sorting
- Aggregate functions (COUNT, SUM, AVG)

### Intermediate
- JOIN operations (INNER, LEFT, RIGHT, FULL)
- GROUP BY and HAVING clauses
- Subqueries and nested SELECT
- Data modification (INSERT, UPDATE, DELETE)

### Advanced
- Common Table Expressions (CTEs)
- Window functions
- Query optimization
- Performance tuning

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify key format starts with 'AIza'
   - Check quota limits in Google AI Studio
   - Test connection in Settings

2. **Query Execution Errors**
   - Check SQL syntax
   - Ensure proper table references
   - Review error messages in results

3. **Installation Issues**
   - Update Python to 3.8+
   - Use virtual environment
   - Install dependencies one by one if needed

### Getting Help
- Check the application logs in the terminal
- Review the browser console for JavaScript errors
- Verify all environment variables are set correctly

## 🔮 Future Enhancements

- **Multi-database Support**: PostgreSQL, MySQL, MongoDB
- **Collaborative Features**: Share queries and results
- **Advanced Visualizations**: Custom chart builder
- **Mobile App**: React Native mobile application
- **Cloud Deployment**: Docker containerization
- **Integration APIs**: Export to BI tools

## 📝 Development Notes

This application demonstrates:
- Modern Flask application architecture
- Secure handling of sensitive data
- Integration with AI services
- Interactive data visualization
- Educational technology principles
- Full-stack web development

The codebase is well-structured for maintenance and extension, with clear separation of concerns and comprehensive error handling.

## 🎉 Getting Started

1. **Run the application**: `python run.py`
2. **Open browser**: http://localhost:5000
3. **Create account**: Register with your details
4. **Add API key**: Get from Google AI Studio and add in settings
5. **Start learning**: Write your first SQL query!

Happy learning! 🚀📊🎯
