# Code Review Assistant

An intelligent code review tool that uses AI to analyze code structure, readability, and best practices, providing detailed feedback and improvement suggestions.

## Features

- **AI-Powered Analysis**: Uses OpenAI GPT-4 to analyze code for readability, modularity, and potential bugs
- **Multiple Input Methods**: Upload files or paste code directly
- **Comprehensive Scoring**: Provides scores for readability, modularity, bug risk, and overall quality
- **Detailed Reports**: Generates detailed analysis reports with specific improvement suggestions
- **Review History**: Stores and displays previous code reviews
- **Modern Web Interface**: Clean, responsive dashboard for easy interaction
- **RESTful API**: Full API for integration with other tools

## Screenshots

The application provides a modern web interface where you can:
- Upload code files or paste code directly
- View comprehensive analysis reports
- See detailed scoring across multiple dimensions
- Access improvement suggestions
- Browse review history

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd code-reviewer-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   DATABASE_URL=sqlite:///./code_reviews.db
   ```

4. **Run the application**
   ```bash
   python -m app.main
   ```

   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   Open your browser and go to `http://localhost:8000`

## Usage

### Web Interface

1. **Upload a file**: Click "Choose File" and select your code file
2. **Or paste code**: Enter a filename and paste your code in the text area
3. **Click "Review Code"**: The AI will analyze your code
4. **View results**: See scores, detailed analysis, and improvement suggestions
5. **Browse history**: Access previous reviews from the sidebar

### API Usage

#### Upload and Review a File
```bash
curl -X POST "http://localhost:8000/api/review" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_code_file.py"
```

#### Review Code from Text
```bash
curl -X POST "http://localhost:8000/api/review-text" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{
    "filename": "example.py",
    "content": "def hello():\n    print(\"Hello, World!\")"
  }'
```

#### Get All Reviews
```bash
curl -X GET "http://localhost:8000/api/reviews" \
  -H "accept: application/json"
```

#### Get Specific Review
```bash
curl -X GET "http://localhost:8000/api/reviews/1" \
  -H "accept: application/json"
```

## API Documentation

The application provides a comprehensive REST API with the following endpoints:

- `POST /api/review` - Upload and review a code file
- `POST /api/review-text` - Review code from text input
- `GET /api/reviews` - Get all code reviews
- `GET /api/reviews/{id}` - Get a specific review by ID
- `DELETE /api/reviews/{id}` - Delete a review
- `GET /health` - Health check endpoint

Visit `http://localhost:8000/docs` for interactive API documentation.

## Architecture

### Backend (FastAPI)
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for storing reviews
- **OpenAI API**: Integration with GPT-4 for code analysis

### Frontend
- **HTML5/CSS3**: Modern, responsive web interface
- **Bootstrap 5**: UI framework for styling
- **Vanilla JavaScript**: Client-side functionality
- **Font Awesome**: Icons

### Database Schema
```sql
CREATE TABLE code_reviews (
    id INTEGER PRIMARY KEY,
    filename VARCHAR,
    file_content TEXT,
    review_report TEXT,
    readability_score FLOAT,
    modularity_score FLOAT,
    bug_risk_score FLOAT,
    overall_score FLOAT,
    suggestions TEXT,
    created_at DATETIME
);
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `DATABASE_URL`: Database connection string (default: SQLite)

### Supported File Types

The application can analyze code in various programming languages:
- Python (.py)
- JavaScript (.js)
- TypeScript (.ts)
- Java (.java)
- C/C++ (.c, .cpp)
- C# (.cs)
- PHP (.php)
- Ruby (.rb)
- Go (.go)
- Rust (.rs)
- Swift (.swift)
- Kotlin (.kt)

## Development

### Project Structure
```
code-reviewer-assistant/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database models and connection
│   ├── models.py        # Pydantic models
│   └── llm_service.py   # OpenAI integration
├── templates/
│   └── index.html       # Main dashboard template
├── static/
│   ├── style.css        # CSS styles
│   └── script.js        # JavaScript functionality
├── requirements.txt     # Python dependencies
├── env.example         # Environment variables template
└── README.md           # This file
```

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables automatic reloading when code changes.

### Testing

You can test the API endpoints using the interactive documentation at `http://localhost:8000/docs` or using curl commands as shown above.

## Deployment

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t code-reviewer-assistant .
docker run -p 8000:8000 -e OPENAI_API_KEY=your_key code-reviewer-assistant
```

### Production Considerations

- Use a production WSGI server like Gunicorn
- Set up proper database (PostgreSQL recommended)
- Configure environment variables securely
- Set up logging and monitoring
- Use HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

## Roadmap

- [ ] Support for more programming languages
- [ ] Integration with popular IDEs
- [ ] Team collaboration features
- [ ] Custom review templates
- [ ] Performance metrics tracking
- [ ] Code quality trends over time
- [ ] Integration with CI/CD pipelines

## Acknowledgments

- OpenAI for providing the GPT-4 API
- FastAPI team for the excellent web framework
- Bootstrap team for the UI framework
- All contributors and users of this project
