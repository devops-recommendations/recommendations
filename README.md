![Build](https://github.com/devops-recommendations/recommendations/actions/workflows/workflow.yml/badge.svg)[![codecov](https://codecov.io/gh/devops-recommendations/recommendations/branch/main/graph/badge.svg?token=O4GINXC92T)](https://codecov.io/gh/devops-recommendations/recommendations)



# Recommendations service.

## Overview

This is the repository that houses the recommendations service that is part of the NYU class **CSCI-GA.2810-001: DevOps
and Agile Methodologies**

## Project Structure

This section explains the general repository structure.

```text
.gitignore                  - this will ignore vagrant and other metadata files
requirements.txt            - list if Python libraries required by your code
config.py                   - configuration parameters

service/                    - service python package
├── __init__.py             - package initializer
├── error_handlers.py       - HTTP error handling code
├── models.py               - module with business models
├── routes.py               - module with service routes
└── status.py               - HTTP status constants

tests/                      - test cases package
├── __init__.py             - package initializer
├── test_models.py          - test suite for busines models
├── test_db_connection.py   - test suite for db connections
├── factories.py            - test factory to instantiate objects for testing
└── test_routes.py          - test suite for service routes

Vagrantfile                 - sample Vagrant file that installs Python 3 and PostgreSQL
```

## Models

This section documents the different data models the service employs.  

#### 1. Recommendation
```text
id: Integer, primary key
product_id: Integer
rec_product_id: Integer
type = <Generic, BoughtTogether, CossSell, UpSell, Complementary>
```

## Dev Setup

1. Clone the repo.
2. Start your Docker Daemon / Virtualbox.
3. From the project root,
    - if you're on an M1 mac, execute `vagrant up --provider docker`
    - if you're on a Windows PC, execute `vagrant up --provider virtualbox`
4. After this, you will find a vm / docker container running on your system, inside which a docker container running
   postgres.

To start the flask app, 
1. run `./scripts/start.sh` from the project directory. This will start the flask app on
   port `5000` in the vm. OR,
2. `vagrant ssh` into the VM; `cd /vagrant`and run `honcho start`

- Server logs will be output in the same terminal window.
- You can check that the service is up and running by executing `curl -X GET http://localhost:5000` from your local shell/terminal.

## Testing the service

From the project root run the following

```shell
vagrant up 

vagrant ssh 

cd /vagrant && nosetests
```

This will generate a coverage and test success report.

## Service Endpoints

#### Get service information

- Endpoint - `GET /`
- Returns - information about the recommendation service
- Command -

```shell
curl -X GET \
  http://localhost:5000/ \
  -H 'cache-control: no-cache'
```

#### Create a new recommendation

- Endpoint - `POST /recommendations`
- Returns - a success status code along with information about the created resource.
- Command -

```shell
curl -X POST \
  http://localhost:5000/recommendations \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"product_id": 1,
	"rec_product_id": 2,
	"type": "Generic"
}'                   
```

#### Get a particular recommendation

- Endpoint - `GET /recommendations/${id}`
- Returns - information about the specified resource
- Command -

```shell
curl -X GET \
  http://localhost:5000/recommendations/1 \
  -H 'cache-control: no-cache'
```

#### Update a recommendation

- Endpoint - `PUT /recommendation/${id}`
- Returns - the updated resource in the body along with a success status code
- Command -

```shell
curl -X PUT \
  http://localhost:5000/recommendations/1 \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{
	"product_id": 1,
	"rec_product_id": 3,
	"type": "Generic"
}'                   
```

#### Delete a recomendation

- Endpoint - `DELETE /recommendations/${id}`
- Returns - Deletes the specified resource
- Command -

```shell
curl -X DELETE \
  http://localhost:5000/recommendations/2 \
  -H 'cache-control: no-cache'
```

#### Get a list of all recommendations

- Endpoint - `GET /recommendations`
- Returns - returns the list of all recommendations for all products
- Command

```shell
curl -X GET \
  http://localhost:5000/recommendations \
  -H 'cache-control: no-cache'
```


#### Get a list of recommendations by Product ID, Recommendation Type, and/or Recommended Product ID

- Endpoint - `GET /recommendations?product_id=${value}&type=${value}&rec_product_id=${value}`
- Returns - return a list of recommendations matching query criteria
- Command -

```shell
curl -X GET \
  http://localhost:5000/recommendations?product_id=1 \
  -H 'cache-control: no-cache'
```

#### Action Route - Increment Interested Counter
- Endpoint - `PUT /recommendations/${id}/interested`
- Returns - increments interested counter for the recommendation with given id
- Command -

```shell
curl -X GET \
  http://localhost:5000/recommendations/1/interested \
  -H 'cache-control: no-cache'
```
