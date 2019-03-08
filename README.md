# Paranuara Challenge
Paranuara is a class-m planet. Those types of planets can support human life, for that reason the president of the Checktoporov decides to send some people to colonise this new planet and
reduce the number of people in their own country. After 10 years, the new president wants to know how the new colony is growing, and wants some information about his citizens. Hence he hired you to build a rest API to provide the desired information.

The government from Paranuara will provide you two json files (located at resource folder) which will provide information about all the citizens in Paranuara (name, age, friends list, fruits and vegetables they like to eat...) and all founded companies on that planet.
Unfortunately, the systems are not that evolved yet, thus you need to clean and organise the data before use.
For example, instead of providing a list of fruits and vegetables their citizens like, they are providing a list of favourite food, and you will need to split that list (please, check below the options for fruits and vegetables).

## New Features
Your API must provides these end points:
- Given a company, the API needs to return all their employees. Provide the appropriate solution if the company does not have any employees.
- Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends in common which have brown eyes and are still alive.
- Given 1 people, provide a list of fruits and vegetables they like. This endpoint must respect this interface for the output: `{"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`

## Delivery
To deliver your system, you need to send the link on GitHub. Your solution must provide tasks to install dependencies, build the system and run. Solutions that does not fit this criteria **will not be accepted** as a solution. Assume that we have already installed in our environment Java, Ruby, Node.js, Python, MySQL, MongoDB and Redis; any other technologies required must be installed in the install dependencies task. Moreover well tested and designed systems are one of the main criteria of this assessement 

## Evaluation criteria
- Solutions written in Python would be preferred.
- Installation instructions that work.
- During installation, we may use different companies.json or people.json files.
- The API must work.
- Tests

Feel free to reach to your point of contact for clarification if you have any questions.

# Solution

## Assumptions

I found 100 companies with index from 0 to 99. However a person in poeple list contains only company_id with a range of 1 to 100. I assumed ```company_id = company.index + 1```.

The API have not authentication mecanism. Authentication is handled by a reverse proxy managed by the Paranuara government.

Environment :
* MongoDB 3.2 is installed and running on localhost:27017 without any authentication mecanism.
* Python 3 is installed
* make command is installed

## Technical choices and architecture

* The people and companies data are store in MongoDB.
* The REST API is built using lightweight Flask library.
    * the configuration from ```config.yml``` file is loaded and stored in Flask config to be available accross every module
    * using Flask config and application context make the application testing easy and prevent circular dependencies 
* unittest library is used for unit and integration tests
    * integration tests define specific database
    * data from this database is removed before each test
    * each test handle its own dataset


## Configuration

You can edit the application configuration before running the following steps according your environment in ```config.yml```:

```yml
mongodb:
  host: localhost # mongodb instance host
  port: 27017 # mongodb instance port
  database: hivery # name of the database in your mongodb instance
doc:
  prefix_uri: /api/docs # context url of the generated API documentation
  spec_uri: http://locahost:5000/api/spec.yml # URL of the API YML specification from the user's browser, if the API is deployed on another server, the server DNS must be used
```

## Setup

From the repository root:

Initialize python virtual environment, install dependencies and load data to the database. The mongodb instance must be started.
```bash
make install
```

Run the application on locahost:5000 :
```bash
make run
```

Resource      | URL              | Description
--------|------------------------|------------------
API URL | http://localhost:5000/ | Root for all the API endpoints
API documentation | http://localhost:5000/api/docs | Interactive Swagger UI documentation for the Paranuara Citizens API
OpenAPI 3.0 Specs | http://localhost:5000/api/spec.yml