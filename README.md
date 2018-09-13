# retail_checkout

This is a small python 3.6 Flask RESTful API application that emulates the 
online-shopping checkout process based on a predefined business logic.

For development purposes the project uses the local file system to store the data
but it has been coded in such way that other DBs such as mongo can be easily integrated 
by extending the data_access package and the DB_Factory class
 
## Dependencies
- python 3.6
- pip
- Docker (only if you want to run the app using docker)

## Run the tests

Clone the project and install the test requirements:
```bash
git clone https://github.com/ldcastell/retail_checkout.git
cd retail_checkout
pip install -r src/test_requirements.txt
cd src
export PYTHONPATH=`pwd`
```

Run the tests:
```bash
# from the src directory
pytest 
```

## Understanding the default Configuration

Under src directory there is a config module which is essentially holding some 
default configurations. The app uses environment variables to override the 
configurations.
some of the current supported environment variables and its default values are:

|Variable| Default | Description| Supported Values |
|--------|---------|------------|------------------|
|RETAIL_STORAGE_BACKEND| "local_fs"| the DB backend to use| "local_fs", ("mongo" in the future)|
|RETAIL_LOCAL_STORAGE_BASE_PATH|"/tmp/data"| only used if using local fs as DB| any valid directory path|
|RETAIL_API_PORT|5000| the port where the API will be served| any valid available port|
|RETAIL_API_LOG_LEVEL|"INFO"| The log level for the app logger| "INFO", "DEBUG", "ERROR", "CRITICAL"|

## Running the application

### Locally running the app:
First install the python dependencies:
```bash
#from the retail_checkout directory
pip install -r src/requirements.txt
``` 

Now you can run the app locally using the local FS as DB by first setting some configurations
like the data directory path:
```bash
#from the retail_checkout directory
export RETAIL_LOCAL_STORAGE_BASE_PATH=`pwd`/data
```
After that you can run the API and test the endpoints
```bash
# From the src directory
python retail_app.py
```

### Running the app with docker

There is also support for Docker in order to run the app in docker you will first need to 
build the image using the provided Dockerfile

```bash
# to build the image with the default configuration run the following 
# command from the retail_checkout directory:
docker build -t retail_checkout_app:0.0.1 -f docker/Dockerfile .
```

Now you can run the app by executing the following command:
```bash
docker run -p 5000:5000 -t retail_checkout_app:0.0.1
```
