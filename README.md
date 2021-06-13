# Flora Plant Service


## Run 

It takes some time to get everything set up and running.

Development version exposes ports for all services to make it easier for development,
other version only exposes port of the main service. 

```shell
# For the real version use, it runs as a deamon
# Note: it takes some time for everything to get up and running please have patience
docker-compose up --build -d

# For development use
docker-compose -f docker/docker-compose-dev.yml up --build 
# Shutdown everything and remove data
docker-compose -f docker/docker-compose-dev.yml down -v 
```

Flora Web Service will be avaiable at: http://localhost:8080

### Authentication

Flora Web Service supports authentication, however since development can be quite hard, this can be disabled. 

To disable authentication change *main/docker/.env.docker* **AUTH_ON** to **false**.

If you are using authentication you can register, get you token and then in the right upper corner click on Authorize, paste your token there and then you can access all of the hidden endpoints.

All of this can be done from postman too, in that case you need to send a 
**Authorization: Bearer <token>** header.

## Docs

You can visit live version of swagger documentation at: http://localhost:8080/docs
