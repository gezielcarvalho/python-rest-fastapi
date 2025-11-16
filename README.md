# Python REST fastAPI

## Description

This is a simple REST API written in Python, using fastAPI and MongoDB, for instrucional purposes only. As for persistence, we use MongoDB as database and Motor for operations. It is developed following an MVC architecture.

## Requirements

- Python 3.8+
- MongoDB 4.4.1+
- fastAPI 0.97.0
- Motor 3.1.2
- Pydantic 1.10.9
- Uvicorn 0.22.0
- Docker & Docker Compose (for containerized deployment)

## Installation

### Option 1: Docker (Recommended)

1. Clone this repository
2. Make sure Docker and Docker Compose are installed
3. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. Build and run the containers:
   ```bash
   docker-compose up --build
   ```
5. Open your browser and go to http://localhost:8000/docs
6. Enjoy!

To stop the containers:

```bash
docker-compose down
```

To stop and remove volumes (database data):

```bash
docker-compose down -v
```

### Option 2: Local Installation

1. Clone this repository
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure MongoDB is running locally
4. Create a `.env` file with your MongoDB connection string
5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
6. Open your browser and go to http://localhost:8000/docs
7. Enjoy!

## Usage

### Create a new user

- Endpoint: /users
- Method: POST
- Body:

```json
{
  "name": "John Doe",
  "email": "john@email.com",
  "password": "123456"
}
```
