# Flora Plant Service


## Run 

It takes some time to get everything set up and running.


Development version exposes ports for all services to make it easier for development,
other version only exposes port of the main service. 

```shell
# For the real version use
docker-compose up --build 

# For development use
docker-compose -f docker/docker-compose-dev.yml up --build 
```