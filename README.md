# Template for a Dockerized WebApp
A template for creating dockerized WebApps using a Python FastAPI backend, and Angular frontend.

# ToDo
* Use alembic (with sqlalchemy?) to setup database connection
    * needs to auto-update the database schemas with every deployment (each time app starts)
    * keep as clean/simple as possible for template

* Explain how to use repo for future use
    * local
        * first terminal
            * `cd backend`
            * `python -m venv .venv`
            * `.venv/scripts/activate`
            * `pip install -r requirements.txt`
            * `python src/app.py`
        * second terminal
            * `ng serve`
            * go to `http://localhost:4200/`
    * container
        * start docker desktop
        * `docker compose up --build`
        * go to `http://localhost:80`

* Setup `launch.json` for debugging locally
