# FastAPI example app

This repository contains code for asynchronous example api using the [Fast Api framework](https://fastapi.tiangolo.com/) ,Uvicorn server and Postgres Database to perform crud operations on notes.

## Installation method 1 (Run application locally)

1. Clone this Repo `git clone (https://github.com/KenMwaura1/Fast-Api-example)`
2. Cd into the Fast-Api folder
   `cd Fast-Api-example`
3. Create a virtualenv
   `python3 -m virtualenv env`
4. Activate virtualenv
   `source /bin/activate`
5. Cd into the src folder
   `cd src`
6. Install the required packages
   `python -m pip install -r requirements.txt`
7. Start the app using Uvicorn
   `uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8002`
8. Ensure you have a Postgres Database running locally.
   Additionally create a Fast_api_dev db with user fast_api having required priviledges
   OR
   Change the DATABASE_URL variable in the .env file to reflect db settings (user:password/db)
9. Check the app on localhost:8002
10. Docs generated on localhost:8002/docs

## Installation method 2 (Run Locally using Docker)

1.Ensure [Docker](https://docs.docker.com/install/) is installed
2.Ensure [Docker Compose](https://docs.docker.com/compose/install/) is installed
3.Clone this Repo
`git clone (https://github.com/KenMwaura1/Fast-Api-example)`

4.`cd Fast-Api-example`

5.Use Docker-Compose to spin up containers `docker-compose up -d --build`

6.If everything completes should be available on localhost:8002

7.Docs are generated on localhost:8002/docs

## Tests

Tests are available using pytest
Run them using `pytest .` while in the root directory (Fast-Api-Example)
