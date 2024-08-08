# Authentication Service (AuthService)

The Authentication Service is a robust solution designed to handle user signups, logins, and authentication. It ensures
secure access control by verifying user credentials and managing user sessions. Additionally, the service includes
functionality to monitor and enforce usage limits, providing both security and user management features. Ideal for
applications requiring reliable user authentication and session management, the Authentication Service streamlines user
account creation and access control.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Deployment](#deployment)

## Features

- **Secure Login and Signup:** Provides robust security for user authentication and registration, ensuring safe and encrypted access.
- **Rate Limiting:** Implements rate limits based on IP addresses and user numbers to prevent abuse and manage traffic effectively.
- **OTP Verification:** Utilizes One-Time Passwords (OTPs) for enhanced security during signup processes.
- **Cache Management:** Leverages Redis for efficient handling of OTPs and session data, improving performance and scalability.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.10+** installed on your machine.
- **Virtualenv** or another method for managing virtual environments.
- **Docker** and **Docker Compose**.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/baharmehri/AuthService.git
cd AuthService
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements/requirements.txt
```

## Environment Variables

Create a .env file in the project root directory and add the required environment.
You can copy the .env.example file:

```bash
cp .env.example .env
```

## Database Migrations

Apply the migrations to set up your database schema:

```bash
python manage.py migrate
```

## Deployment

To deploy the Notification Service using Docker Compose, run this:

```bash
docker compose up --build -d
```