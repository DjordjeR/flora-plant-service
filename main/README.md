# main_service

## Run

**run docker compose**

* Copy *.env.example* to *.env*
* Fill in necessary credentials (if you are using docker-compose skip this step)

```shell

# To start main service
cd src
uvicorn app.main:app --reload
```