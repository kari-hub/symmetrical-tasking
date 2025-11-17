# Task Manager API

A modern FastAPI-based task management application with user authentication, role-based access control, and PostgreSQL database integration.

## ✨ Features

- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **Task Management**: Full CRUD operations for tasks with priorities and status tracking
- **User Management**: User registration, profile management, and account operations
- **Database Migrations**: Alembic-powered schema versioning and management
- **Automated Testing**: Comprehensive CI/CD pipeline with GitHub Actions
- **Type Safety**: Static type checking with MyPy
- **Code Quality**: Automated linting with Ruff

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 15 or higher
- pip or poetry for dependency management

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory with the following variables:

   ```env
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/database_name
   SECRET_KEY=your-secret-key-minimum-32-characters
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRY_MINUTES=30
   ```

   > **Security Note**: Generate a strong SECRET_KEY using:
>
   > ```bash
   > python -c "import secrets; print(secrets.token_urlsafe(32))"
   > ```

5. **Initialize the database**

   ```bash
   alembic upgrade head
   ```

6. **Start the development server**

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://localhost:8000`

   Interactive API documentation: `http://localhost:8000/docs`

## 📚 API Documentation

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/login` | Authenticate user and receive JWT token | No |

### User Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/register` | Create a new user account | No |
| `GET` | `/users/` | Retrieve all users | No |
| `GET` | `/user/{user_id}` | Retrieve specific user details | No |
| `PATCH` | `/user/{user_id}` | Update user profile | Yes |
| `DELETE` | `/user/{user_id}` | Delete user account | Yes |

### Task Management

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/tasks` | Create a new task | Yes |
| `GET` | `/tasks` | Retrieve all tasks | No |
| `GET` | `/tasks/{task_id}` | Retrieve specific task | No |
| `PATCH` | `/tasks/{task_id}` | Update task details | Yes |
| `DELETE` | `/tasks/{task_id}` | Delete a task | Yes |

## 🔐 Authentication Flow

1. **Register** a new user account via `/register`
2. **Login** via `/login` with email and password to receive an access token
3. **Authenticate** requests by including the token in the Authorization header:

   ```
   Authorization: Bearer <your_jwt_token>
   ```

### Example Authentication

```bash
# Register
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'

# Login
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john@example.com&password=SecurePass123!"

# Use the returned token for authenticated requests
curl -X POST http://localhost:8000/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Update README and API docs",
    "status": "todo",
    "priority": "high"
  }'
```

## 📊 Data Models

### User

- Unique username and email
- Securely hashed password
- One-to-many relationship with tasks

### Task

- Title and description
- Timestamps (created_at, due_at)
- Status tracking (TODO, IN_PROGRESS, COMPLETED)
- Priority levels (LOW, MEDIUM, HIGH)
- Completion flag
- Owner relationship to User

## 🛠️ Development

### Running Tests

```bash
pytest -v
```

### Code Quality Checks

```bash
# Linting
ruff check .

# Type checking
mypy . --explicit-package-bases --install-types --non-interactive --ignore-missing-imports
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1
```

## 📦 Technology Stack

- **[FastAPI](https://fastapi.tiangolo.com/)**: High-performance web framework
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: SQL toolkit and ORM
- **[Pydantic](https://docs.pydantic.dev/)**: Data validation using Python type hints
- **[Alembic](https://alembic.sqlalchemy.org/)**: Database migration tool
- **[PostgreSQL](https://www.postgresql.org/)**: Robust relational database
- **[python-jose](https://python-jose.readthedocs.io/)**: JWT implementation
- **[Passlib](https://passlib.readthedocs.io/)**: Password hashing library
- **[Uvicorn](https://www.uvicorn.org/)**: Lightning-fast ASGI server

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and ensure tests pass
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please ensure:

- All tests pass (`pytest`)
- Code passes linting (`ruff check .`)
- Type checking passes (`mypy .`)
- Follow the existing code style

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📧 Support

For questions or support, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI and Python**
