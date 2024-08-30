# GovTech Assignment

## Task 1 Backend

First, navigate to the backend folder with the command:

```bash
cd backend
```

### Getting Started

You need to create a .env file in the top level of the backend folder with the following content:

```bash
OPENAI_API_KEY="YOUR_OPENAI_SECRET_KEY"
```

This backend is designed to run with Docker Compose, which sets up two containers:

1. **MongoDB** running on `localhost:27018`
2. **Backend API** running on `localhost:8000`

To run the backend with Docker, use the following command:

```bash
docker-compose up --build -d
```

This command will build the Docker images and start the containers in detached mode.

### Accessing the API

Once the containers are running, you can try the FastAPI docs by navigating to:

```bash
http://localhost:8000/docs
```

### Testing the backend

To run the tests with no warnings, run the command:

```bash
pytest -p no:warnings
```
