# AstroDB 🚀

Hey, wouldn't it be great if there was a comprehensive database of everyone who has ever been into space?

I think so too, so this project was created primarily to try and scrape a number of different data sources to pull all of this information togeter. (It was also created to play around with a number of Python data processing and visualisation libraries)

## Getting Started

This project makes use of the [opinionated Docker images provided by Jupyter](https://github.com/jupyter/docker-stacks)

Start the notebook by simply running

```
docker compose up
```

or alternatively

```
#For Windows using a MinGW shell
winpty docker run -it --rm -p 8888:8888 -v /$PWD:/home/jovyan jupyter/datascience-notebook

#For Mac/Linux
docker run -it --rm -p 8888:8888 -v $PWD:/home/jovyan jupyter/datascience-notebook
```

### Prerequisites

* Docker
* Docker Compose

## Built With

* [Docker/Docker Compose](https://www.docker.com/) - Used for managing the environment. 
* [Jupyter](http://jupyter.org/) - Notebook server.  The Jupyter docker image used contains loads of great python resources

## Acknowledgments

* Jonny O'C for the great idea
* Wikipedia for having the answers to all the questions