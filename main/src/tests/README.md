# tests

## Run

***Tests without authenthication -> AUTH_ON=false***

Directory /tests_py contains all tests for requests, everything else is started and regulated with the provided scripts.
Don't run the tests quickly one after the other! Wait a little so that the services can be stopped fully.
Also, the tests take some time to start due to the setup of the docker containers and wait for initialisation time.

* test_base.sh - tests every request in a scenario where every service should be working (no search tests included here)
* test_no_auth.sh - will stop the keycloak service and test the authentication requests
* test_search.sh - test the search service and available results
* test_no_search.sh - will stop the search service and test the available search feature and other requests


***Tests with authenthication -> AUTH_ON=true***

* test_AUTH_ON.sh - same as test_base.sh but it uses the token as authenthication, this tests also the refresh token feature
