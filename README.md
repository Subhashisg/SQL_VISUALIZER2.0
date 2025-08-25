# Flask SQL Visualizer

A Flask-based AI-powered SQL visualizer that helps users learn SQL interactively with Google Gemini AI integration.

## Features

- User authentication and secure API key storage
- Interactive SQL query execution and visualization
- AI-powered table creation and sample data generation
- Visual representation of SQL operations
- Secure encrypted storage of API keys

## Setup

1. Create virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment variables file:
```bash
copy .env.example .env
```

4. Run the application:
```bash
python run.py
```

## Usage

1. Register/Login to the application
2. Add your Google Gemini API key in settings
3. Start writing SQL queries
4. Let AI create tables and sample data automatically
5. Visualize query results and operations

## Security

- API keys are encrypted before storage
- Secure user authentication with Flask-Login
- SQL injection protection
- Session management
