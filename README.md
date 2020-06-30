# Web API Backends
Getting a better understanding of some web API backends.

Exploring:

- Flask
    - Restless
    - GraphQL

## How to use

First, make sure to [install and configure Docker](https://docs.docker.com/docker-for-mac/install/).

Then, clone this repo.

Finally, open a terminal and `cd` into the repo, then run:

```
docker-compose build
docker-compose up
```

Currently, you should be able to access the endpoint `dtc` at `http://localhost:5000/api/dtc`, which the ability to access individual records by id, e.g. `http://localhost:5000/api/dtc/1520`
