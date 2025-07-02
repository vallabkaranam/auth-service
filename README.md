# 🔐 Enterprise Authentication Microservice

A production-ready authentication microservice built with FastAPI, featuring secure JWT-based authentication, role-based access control, and modern security practices. Designed for seamless integration into larger systems, this service provides a robust foundation for user management and authentication.

http://auth-service-alb-241967298.us-east-1.elb.amazonaws.com/docs (service was spun down as of July 1, 2025, to preserve resources — read more [here](https://medium.com/@vallab.karanam/how-i-brought-my-aws-ecs-bill-from-45-to-almost-0-without-sacrificing-my-architecture-aeb75058af8c))

## ✨ Key Features

- 🔒 **Secure Authentication**

  - JWT-based authentication with access and refresh tokens
  - Password hashing with bcrypt
  - Token expiration and refresh mechanisms
  - Secure password validation and complexity requirements
  - Google OAuth integration (Coming Soon)

- 👥 **User Management**

  - Email/password registration and login
  - Role-based access control (RBAC)
  - User profile management

- 🛡️ **Security Best Practices**
  - OAuth2 password flow implementation
  - JWT token validation and verification
  - Secure session management
  - Protection against common security vulnerabilities

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT, OAuth2
- **Password Hashing**: bcrypt
- **API Documentation**: OpenAPI (Swagger)
- **Environment Management**: python-dotenv
- **Containerization**: Docker
- **Database Management**: pgAdmin

## 🚀 Getting Started (Local Development)

This section guides you through setting up and running the service on your local machine for development and testing.

### Prerequisites

- Python 3.11+
- Docker
- pgAdmin (optional, for database management)
- pip (Python package manager)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/auth-service.git
cd auth-service
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
```

Update the .env file with your local database credentials and JWT secrets. The default values should work with the provided Docker setup.

Required environment variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db
ACCESS_TOKEN_SECRET_KEY=your_access_token_secret
REFRESH_TOKEN_SECRET_KEY=your_refresh_token_secret
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
```

5. Start the PostgreSQL database:

```bash
docker start fastapi-postgres
```

If you haven't created the PostgreSQL container yet, you can create it with:

```bash
docker run --name fastapi-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=auth_db -p 5432:5432 -d postgres
```

*(Note: The `-e POSTGRES_USER=user` and `-e POSTGRES_PASSWORD=password` flags are intentionally set to match the example `DATABASE_URL` from your `.env` file. This ensures your application can connect to the local database seamlessly.)*

6. Run database migrations:

```bash
alembic upgrade head
```

7. Start the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## ☁️ Cloud Deployment

This service is architected for a secure and scalable production deployment on AWS.

**Platform**: The application is deployed as a container on **AWS ECS Fargate**, providing a serverless compute environment.

**Database**: The production environment uses a managed **AWS RDS for PostgreSQL** instance, running in private subnets for security.

**Container Registry**: The official Docker image is stored in **Amazon ECR (Elastic Container Registry)** at the following URI:
`640168435590.dkr.ecr.us-east-1.amazonaws.com/auth-service`

**Networking**: An **Application Load Balancer (ALB)** manages incoming web traffic, routing it to the ECS service. The ALB resides in public subnets, while the ECS tasks run in private subnets.

**Configuration**: All production environment variables (like `DATABASE_URL` and JWT secrets) are managed securely through **AWS Secrets Manager** and injected into the ECS Task at runtime. The task definition itself contains no plaintext secrets.

For a complete, step-by-step guide on the entire cloud deployment process, please refer to the canonical deployment guide.

## �� API Documentation

Interactive API documentation is available at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

- `POST /api/v1/auth/signup` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/admin/users` - Admin-only: List all users

## 📁 Project Structure

```
auth-service/
├── alembic/              # Database migrations
├── app/
│   ├── controllers/      # Business logic
│   ├── db/              # Database models and session
│   ├── dependencies/     # FastAPI dependencies
│   ├── interfaces/      # Data access layer
│   ├── routes/          # API endpoints
│   ├── schemas/         # Pydantic models
│   └── utils/           # Utility functions
├── requirements.txt      # Project dependencies
└── alembic.ini          # Alembic configuration
```

## 🔐 Authentication Flow

1. **Registration**

   - User submits email and password
   - Password is validated and hashed
   - User record is created in the database
   - Access and refresh tokens are issued

2. **Login**

   - User submits credentials
   - Credentials are verified
   - New access and refresh tokens are issued

3. **Token Refresh**
   - User submits refresh token
   - Token is validated
   - New access and refresh tokens are issued

## 🎯 Why This Matters

This project demonstrates several important aspects of modern backend development:

- **Microservices Architecture**: Designed as a standalone service that can be easily integrated into larger systems
- **Security First**: Implements industry-standard security practices and token-based authentication
- **Scalability**: Built with performance and scalability in mind using FastAPI and SQLAlchemy
- **Maintainability**: Clean architecture with clear separation of concerns
- **Production Ready**: Includes proper error handling, logging, and a deployment model that separates configuration from code

## 📝 License

MIT License - feel free to use this project as a reference or starting point for your own authentication service.
