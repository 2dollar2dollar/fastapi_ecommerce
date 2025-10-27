# 🛒 FastAPI Ecommerce

Asynchronous REST API for an e-commerce platform built with FastAPI, PostgreSQL, JWT authentication, and full CRUD operations.

## 🚀 Features

- **🔐 JWT Authentication** - secure login/registration system
- **⚡ Asynchronous Requests** - high performance with async/await
- **🐘 PostgreSQL** - reliable relational database
- **SQLAlchemy 2.0+** - modern async ORM
- **Alembic** - database migrations
- **Pydantic v2** - data validation
- **CRUD Operations** for products, categories, users, and reviews
- **RESTful API** - REST principles compliance

## 📁 Project Structure

```
fastapi_ecommerce/
├── app/
│   ├── migrations/          # Database migrations (Alembic)
│   │   └── versions/
│   ├── models/             # SQLAlchemy models
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── categories.py
│   │   └── reviews.py
│   ├── routers/            # API endpoints
│   │   ├── users.py
│   │   ├── products.py
│   │   ├── categories.py
│   │   └── reviews.py
│   ├── auth.py            # JWT authentication
│   ├── config.py          # Application configuration
│   ├── database.py        # Async database setup
│   ├── db_depends.py      # Database dependencies
│   ├── schemas.py         # Pydantic schemas
│   └── main.py           # FastAPI main application
├── requirements.txt
└── alembic.ini
```

## 🛠 Technologies

- **Python 3.8+**
- **FastAPI** - modern, fast web framework
- **PostgreSQL** - relational database
- **SQLAlchemy 2.0+** - asynchronous ORM
- **Alembic** - database migration system
- **JWT** - authentication
- **Pydantic v2** - data validation
- **Uvicorn** - ASGI server
- **AsyncPG** - async driver for PostgreSQL
- **Python-multipart** - form data handling

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### 2. Clone Repository
```bash
git clone https://github.com/yourusername/fastapi_ecommerce.git
cd fastapi_ecommerce
```

### 3. Create Virtual Environment
```bash
python -m venv .venv

# Activation (Linux/Mac)
source .venv/bin/activate

# Activation (Windows)
.venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. PostgreSQL Setup
```sql
-- Create database
CREATE DATABASE fastapi_ecommerce;

-- Create user (optional)
CREATE USER fastapi_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE fastapi_ecommerce TO fastapi_user;
```

### 6. Environment Configuration
Create `.env` file in project root:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/fastapi_ecommerce
SYNC_DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_ecommerce

# JWT
SECRET_KEY=your-secret-key-here-make-it-very-long-and-secure
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# App
DEBUG=true
```

### 7. Apply Migrations
```bash
# Create migrations (when models change)
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 8. Run Application
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

After starting the application, automatic documentation is available:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `POST /auth/token` - Get JWT token

### Users
- `GET /users/me` - Get current user
- `GET /users/` - List users (admin only)
- `PUT /users/{id}` - Update user

### Products
- `GET /products/` - List products (pagination, filtering)
- `GET /products/{id}` - Get product by ID
- `POST /products/` - Create product (authentication required)
- `PUT /products/{id}` - Update product (authentication required)
- `DELETE /products/{id}` - Delete product (admin only)

### Categories
- `GET /categories/` - List categories
- `POST /categories/` - Create category (authentication required)

### Reviews
- `GET /reviews/` - List reviews
- `GET /reviews/product/{product_id}` - Get product reviews
- `POST /reviews/` - Create review (authentication required)

## 🗄 Database Models

- **Users** - system users (id, email, username, hashed_password, is_active, is_admin)
- **Products** - store products (id, name, description, price, category_id, created_at)
- **Categories** - product categories (id, name, description)
- **Reviews** - product reviews (id, product_id, user_id, rating, comment, created_at)

## 🔧 Development Configuration

### Production Environment Variables
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname
SECRET_KEY=very-long-and-secure-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=false
```

## 🤝 Development

### Creating New Migrations
```bash
# After model changes
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

## 🚀 Performance

- Asynchronous database queries with asyncpg
- Connection pooling for PostgreSQL
- Caching for frequently requested data
- Optimized SQL queries