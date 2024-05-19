# BaseDjango
This project provides a foundational application with user authentication and PostgreSQL integration. Currently under development, it offers a Docker Compose setup for easy local testing.

# Features
- **Secure User Authentication:** Implements JWT based authentication for robust access control.
- **Comprehensive User Management:** Provides CRUD (Create, Read, Update, Delete) functionalities for managing user data.
- **Interactive API Documentation:** Offers clear and interactive API documentation using Swagger, simplifying integration for developers.
- **Enhanced Login Security:** Enables secure login via email using one-time passwords (OTP) stored on Redis for added protection.
- **PostgreSQL Database Integration:** Leverages PostgreSQL for reliable and scalable data storage and management.
- **Automated Testing:** Includes integration test cases to ensure code quality and application functionality.

# Instructions
To run the application using Docker Compose, follow these steps:

1.Clone the repository to your local machine:

`git clone <repository-url>`

2.Navigate to the project directory:

`cd base_django`

3.Build and run the Docker containers using Docker Compose:

`docker compose up`

After successfully launching the containers with Docker Compose, you can access the application in your web browser at `http://localhost:8000`.

# Technologies Used
- Python
- Django
- PostgreSQL
- Redis
- Swagger
- Docker
- Docker Compose
- REST framework for API development