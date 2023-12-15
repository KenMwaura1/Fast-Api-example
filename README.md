# FastAPI Example App

![fastapi-0.104.1-informational](https://img.shields.io/badge/fastapi-0.104.1-informational) [![CodeQL](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/codeql.yml/badge.svg)](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/codeql.yml)
[![Docker Compose Actions Workflow](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/docker-image.yml/badge.svg)](https://github.com/KenMwaura1/Fast-Api-example/actions/workflows/docker-image.yml)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/kenmwaura1)
[![Twitter](https://badgen.net/badge/icon/twitter?icon=twitter&label=Follow&on)](https://twitter.com/Ken_Mwaura1)

This repository contains code for asynchronous example api using the [Fast Api framework](https://fastapi.tiangolo.com/) ,Uvicorn server and Postgres Database to perform crud operations on notes.

![Fast-api](images/fast-api-scrnsht-1.png)

## Accompanying Article

Read the full tutorial [here](https://dev.to/ken_mwaura1/getting-started-with-fast-api-and-docker-515)

## Installation method 1 (Run application locally)

1. Clone this Repo

   `git clone (https://github.com/KenMwaura1/Fast-Api-example)`
2. Cd into the Fast-Api folder

   `cd Fast-Api-example`
3. Create a virtual environment

   `python3 -m venv venv`
4. Activate virtualenv

   `source venv/bin/activate`

   For zsh users

   `source venv/bin/activate.zsh`

   For bash users

   `source venv/bin/activate.bash`

   For fish users

   `source venv/bin/activate.fish`
5. Cd into the src folder

   `cd src`
6. Install the required packages

   `python -m pip install -r requirements.txt`
7. Start the app

   ```shell
   python main.py
   ```

   7b. Start the app using Uvicorn

   ```shell
   uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8002
   ```

8. Ensure you have a Postgres Database running locally.
   Additionally create a `fast_api_dev` database with user `**fast_api**` having required privileges.
   OR
   Change the DATABASE_URL variable in the **.env** file inside then `app` folder to reflect database settings (user:password/db)

9. Check the app on [notes](http://localhost:8002/notes)
Open your browser and navigate to [docs](http://localhost:8002/docs) to view the swagger documentation for the api.

## Vue Frontend (Optional)

The is a simple Vue frontend using [vite](https://vitejs.dev/guide/) that was added. However it is an optional step in running the application.

### Installation

Ensure you have [Node.js](https://nodejs.org/en/) installed. any version above 16 should work.

While inside the root folder `Fast-Api-example`

1. Cd into the `vue-client` folder.

   ```shell
      cd vue-client
      ```

2. Install the required dependencies.
   for NPM:

   ```shell
      npm install
      ```

   for Yarn:

   ```shell
      yarn install
      ```

3. Start the Vue app
   for NPM:

   ```shell
      npm run serve
      ```

   for Yarn:

   ```shell
      yarn serve
      ```

4. Open your browser and navigate to [notes](http://localhost:5173)

## Installation method 2 (Run Locally using Docker)

1. Ensure [Docker](https://docs.docker.com/install/) is installed.

2. Ensure [Docker Compose](https://docs.docker.com/compose/install/) is installed.

3. Clone this Repo

   `git clone (https://github.com/KenMwaura1/Fast-Api-example)`

4. Change into the directory

   ```cd Fast-Api-example```

5. Use Docker-Compose to spin up containers

   `docker-compose up -d --build`

6. If everything completes should be available on [notes](http://localhost:8002/notes)

7. Docs are generated on [docs](http://localhost:8002/docs)

## Tests

Tests are available using pytest
Run them using `pytest .` while in the root directory (/Fast-Api-example)

## Documentation

Open API Documentation is provided by [Redoc](http://localhost:8002/redoc)

## Contributing

Contributions are welcome, please open an issue or submit a PR.

## Github Actions

Github actions are used to run tests and build the docker image. The docker image is pushed to [Docker Hub](https://hub.docker.com/repository/docker/kenmwaura1/fast-api-example). Inorder to effectively use the actions you will need to add the following secrets to your repository settings. `DOCKER_USERNAME` and `DOCKER_PASSWORD` for the docker hub account.
This is to enable the docker login step in the workflow and push the image to the docker hub repository. Alternatively you can remove the step from the workflow by commenting it out.

It is also possible to use [Github Packages](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-docker-registry) to store the docker image. In this case you will need to add the following secrets to your repository settings. `CR_PAT` and `CR_USERNAME` for the github packages account. In our case the username is the github username. The `CR_PAT` is a personal access token with the `write:packages` scope. This is to enable the docker login step in the workflow and push the image to the github packages repository. Alternatively you can remove the step from the workflow by commenting it out.

The docker image is also tagged with the commit sha and pushed to the docker hub repository. This is to enable the image to be pulled by the docker-compose file in the root directory. The docker-compose file is used to spin up the containers locally. It is available on [Github Packages](https://github.com/KenMwaura1/Fast-Api-example/pkgs/container/fast-api-example) as well.

## Docker Hub

The docker image is available on [Docker Hub](https://hub.docker.com/repository/docker/kenmwaura1/fast-api-example)

## License

[MIT](https://choosealicense.com/licenses/mit/)
