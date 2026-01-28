# Blog Management System

A FastAPI-based blog management system with user management, blog CRUD operations, file handling, and AI chat capabilities.

## Features

- **User Management**: Create and list users with unique username validation
- **Blog CRUD Operations**: Create, read, update, and delete blogs with user authorization
- **File Upload/Download**: Upload files and download them via API endpoints
- **Job Application**: Submit job applications with form data and CV file upload
- **AI Chat**: Integrated LangChain AI chat functionality (currently disabled)

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM for database operations
- **SQLite**: Lightweight database for development
- **LangChain**: AI/LLM integration framework
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI

## Project Structure

```
PIP_Blog_mng_syt/
├── db/
│   └── database.py          # Database configuration and session management
├── routers/
│   ├── blog.py              # Blog CRUD endpoints
│   ├── user.py              # User management endpoints
│   ├── handle_file.py       # File upload/download and job application endpoints
│   └── ai_chat.py           # AI chat endpoints (currently disabled)
├── files/                   # Directory for uploaded files
├── main.py                  # FastAPI application entry point
├── models.py                # SQLAlchemy database models
├── schema.py                # Pydantic schemas for request/response validation
├── requirements.txt         # Python dependencies
└── pyproject.toml           # Project configuration

```

## Setup Instructions

### Prerequisites

- Python 3.12 or higher
- pip or uv package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PIP_Blog_mng_syt
```

2. Install dependencies:
```bash
# Using pip
pip install -r requirements.txt

# Or using uv
uv sync
```

3. Set up environment variables (if needed):
Create a `.env` file in the root directory for any required environment variables (e.g., API keys for AI chat).

4. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

5. Access API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Users

- `POST /users` - Create a new user
  - Request body: `{ "username": "string", "email": "string" }`
  - Returns: Created user object

- `GET /users` - Get all users
  - Returns: List of all users

### Blogs

- `POST /blogs` - Create a new blog post
  - Query parameter: `user_id` (required)
  - Request body: `{ "title": "string", "content": "string" }`
  - Returns: Created blog object

- `GET /blogs` - Get all blogs for a user
  - Query parameter: `user_id` (required)
  - Returns: List of blogs for the specified user

- `GET /blogs/{id}` - Get a specific blog post
  - Path parameter: `id` (blog ID)
  - Query parameter: `user_id` (required)
  - Returns: Blog object (only if owned by the user)

- `PUT /blogs/{id}` - Update a blog post
  - Path parameter: `id` (blog ID)
  - Query parameter: `user_id` (required)
  - Request body: `{ "title": "string", "content": "string" }`
  - Returns: Updated blog object

- `DELETE /blogs/{id}` - Delete a blog post
  - Path parameter: `id` (blog ID)
  - Query parameter: `user_id` (required)
  - Returns: Success message

### Files

- `POST /file/upload` - Upload a file
  - Form data: `upload_file` (file)
  - Returns: `{ "filename": "string", "message": "File Uploaded successfully" }`

- `GET /file/download` - Download a file
  - Query parameter: `name` (filename)
  - Returns: File download

- `POST /file/apply` - Submit a job application
  - Form data:
    - `name` (string, required)
    - `email` (email, required)
    - `phone` (string, required)
    - `address` (string, required)
    - `experience` (integer, required)
    - `linkedin_url` (URL, optional)
    - `cv` (file, required)
  - Returns: Application details

### Static Files

- Files uploaded via the API are accessible at `/files/{filename}`

## Database

The application uses SQLite database (`blog_mng.db`) which is automatically created on first run. The database contains two main tables:

- **users**: Stores user information (id, username, email)
- **blogs**: Stores blog posts (id, title, content, user_id)

## Development

The application uses SQLAlchemy ORM for database operations and Pydantic for data validation. Database models are defined in `models.py` and schemas are defined in `schema.py`.

## License

[Add your license information here]
