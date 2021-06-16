# tests

## Run

**Before running the tests start the main service**

Directory /tests_py contains all tests for requests, everything else is started and regulated with the provided scripts.

* test_base.sh - tests every request in a scenario where every servise should be working
* test_no_auth.sh - will stop the keycloak service and test the authentication requests

