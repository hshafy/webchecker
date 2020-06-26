# Webchecker

This is a system that monitors website availability over the
network, produces metrics about it and passes these events through 
Kafka topic into PostgreSQL database.

For this, we have a Kafka producer which periodically checks the target
websites and sends the check results to a Kafka topic, and a Kafka consumer
storing the data to a PostgreSQL database.

## Design 

The system consists of the following components:

* Scheduler
* Webchecker 
* Writer
* Transport

The Scheduler owns the websites' data including the frequency of checking
them. 

The checker performs checks, collect response time, error code returned, and decide if the check passed/failed
depending on the configuration and then pass the events to a trasnport.

The writer listens to the trasnport and write events to a database.

The trasnport is a pub/sub system that holds messages and allow subscripers to
consume messages published by a producer.

### Tech Stack

In this system we use:

* Python 3.7
* PostgresSQL
* Kafka
* Zookeeper
* psycopg2
* [kafka-python](https://github.com/dpkp/kafka-python)
* Docker
* [Poetry](https://python-poetry.org)

## Development

### Tests

In this project we use Poetry for packaging and dependency management, make
sure you have it [installed](https://python-poetry.org/docs/#installation) on your system.

install dependencies and activate virtual env
```
poetry install
poetry shell
```

run tests

```
make test
```

Run tests with coverage report
```
make test-cov
```

### Running the full stack

We use docker-compose to get the full stack up and running locally, to run the
full stack that include writer, checker, postgres, kafka and zookeeper containers
run:
```
make up
```

To tail the logs run:
```
make logs
```

The checker will create the database when doesn't find it, and
kafka will create the required topic, so no more steps needed to have the full system
running on your machine.

The system will start checking sites from the settings file, more configuration
can be found in the settings file.


## Deployment

The system is fully operational locally, however it's still not production ready, it's planned to be deployed on the Aiven.io but still need few iterations, for a list of the planned work and project roadmap check the Roadmap section below. 

## Roadmap

Planned work and WIP list:

* Add [celery beat](https://docs.celeryproject.org/en/stable/userguide/periodic-tasks.html) and [redbeat](https://github.com/sibson/redbeat) to handle more reliable and distributed scheduler that can run on multiple nodes, scheduler task will only send messages to a broker, that the checker's worker(s) listen to, and start checking websites, currently a very simple scheduler implemented that only check one website with a predefined check frequency.
* Handle workers life cycle.
* Use connection pool for the accessing the database
* Add CI/CD
* Add more tests coverage
* Move parts of the settings to env variables
* Add REST APIs on top of the scheduler to manage websites subscriptions
* Add regex body checks
* Add terraform to create production and staging environments
