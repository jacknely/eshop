# eShop Endpoint
Flask application that creates an endpoint for shop metrics on a given date. 

## Requirements
- Python 3.6.5 to 3.8.1
- Docker
- Flask
- Flask-RESTful
- Pandas
- Pathlib
- Pytest


All requirements are installed from requirements.txt during docker container build.

## Build and Run
### Option 1: Docker Compose
Execute the following code in root directory of application
```
docker-compose up
```


### Option 2: Docker
To build image, navigate to application root folder and execute the below code:
```
docker build -t eshop:latest .
```
An internet connection is required to download 'python:3.8-slim' base image.

Once image has been created, execute the below code to run the container:
```
docker run -d -p 5000:5000 eshop
```

## Usage
With the container running, navigate to the below address in browser:
```
http://localhost:5000/<date>
```
where < date > is in YYYY-MM-DD format

This will return the below endpoint for the given date:
```
{
    "customers": 10,
    "items": 123,
    "order_total_avg": 1341449.56,
    "discount_rate_ave": 0.13,
    "commissions": {
        "promotions": {
            "1.0": 819302.4,
            "3.0": 64855.08,
            "4.0": 19995.2
        },
        "total": 22358623.33,
        "order_average": 22358623.33
    }
}
```

#### Example 1
To retrieve data for 13th May 2019, the below should be entered into browser address bar:
```
http://127.0.0.1:5000/2019-05-13
```

## Tests
Run the test suite by executing the below command in application root folder:
```
pytest tests
```
If running tests inside dockerised container then, when container is running, execute the below code:
```
docker exec -it eshop_eshop_1 py.test  
```