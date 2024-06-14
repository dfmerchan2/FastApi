# ****_Project Bookstore_****


## Start:
* You need to open your virtual environment to install the dependencies 
* Install poetry if you don't have poetry in your venv - `pip install poetry `
* Install dependencies - `poetry install` 
* If you have any message that you need to run the lock - `poetry lock --no-update`

## Run Test:

#### For run unit test for services
* You need to use two environment variable to mock the DB Session (ENV and MODE_TEST)
* Run the command: `ENV=TESTING MODE_TEST=Unit pytest -m unit`

#### For run unit test for apis 
* You need to use two environment variable to mock the DB Session (ENV and MODE_TEST)
* Run the command: `ENV=TESTING MODE_TEST=Unit pytest -m api`

#### For run apis test without mocks ***WIP
* You need to use two environment variable to create the DB Session (ENV and MODE_TEST)
* Run the command: `ENV=TESTING MODE_TEST=develop pytest -m test`


## RUN Apis:
* To run the project apis, you can run command : `uvicorn  main:app --reload --port 5001`
* By default you can use _ENV=DEVELOPMENT_ and _MODE_TEST=develop_, to create the real DB 