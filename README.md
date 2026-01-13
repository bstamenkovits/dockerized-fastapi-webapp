# Template for a Dockerized WebApp
A template for creating dockerized WebApps using a Python FastAPI backend, and Angular frontend.

# ToDo
* Add tests

* connect frontend to database call

* Add a docs folder in which the general setup is explained

* move config.py to util/config.py and define configs in config.ini

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
