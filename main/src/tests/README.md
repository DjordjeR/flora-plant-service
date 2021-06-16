# tests

## Run

***Be sure to set the AUTH_ON variable in the .env file to FALSE!!!***

Directory /tests_py contains all tests for requests, everything else is started and regulated with the provided scripts.
Also the tests may run a little slow due to the setup of the docker containers and wait for initialisation times.

* test_base.sh - tests every request in a scenario where every service should be working (no search tests included here)
* test_no_auth.sh - will stop the keycloak service and test the authentication requests
* test_search.sh - test the search service and available results
* test_no_search.sh - will stop the search service and test the available search feature and other requests


***Base test with authenthication -> set AUTH_ON=true***

* test_AUTH_ON.sh - same as test_base.sh but with AUTH_ON set to true in .env
