# Setup
This document goes over how to install the dependencies for this project, and how to run the application (both locally and as a docker container)

## Prequisites:
### Local Development
* Backend
    * Python 3.11
* Frontend
    * node 22
* Database
    * SQLite

### Docker
* Docker Engine (comes with Docker Desktop)

## Local Development
When developping locally, or if you want to run the application natively, the following steps need to be undertaken

### Backend
The backend runs a FastAPI web app, for this a virtual environment should be created, in which all of the dependencies can be installed.

Begin by opening a terminal in the root directory of this project.

1) Navigate to backend

```bash
cd backend
```

2) Create a Python virtual environment
```bash
python venv .venv
```

3) Activate virtual environment

```bash
# Windows
.venv/scripts/activate

# MacOS/Linux
source .venv/bin/activate
```

4) Install dependencies
```bash
pip install -r requirements.txt
```

5) Run FastAPI app
```bash
python src/app.py
```

The backend of the application will be running on `http://localhost:8000`, you do not need to visit this address, this is just the root of all of the backend endpoints that the frontend angular application will use.

### Frontend
The frontend is an Angular application. Node.js and npm are required to install dependencies and run the development server.

While keeping the terminal with the backend running open, open a new terminal (again in the root of this project).

1) Navigate to frontend

```bash
cd frontend
```

2) Install dependencies

```bash
npm install
```

3) Run the development server

```bash
ng serve
```

The application will be available at `http://localhost:4200`, if the [backend](#backend) is running, then this address should lead to the angular web app.

## Docker Compose
Make sure Docker Engine is running (simply launch Docker Desktop if that's installed).

The first time you run this application in its dockerized form, you will need to build all the relevant images.

```bash
docker compose up --build
```

After having done this at least once you can simply run

```bash
docker compose up
```

In both cases the application can be accessed at `http://localhost:4200`
