# tests

## Run

**Before running the tests, start the main service**

Directory /tests_py contains all tests for requests, everything else is started and regulated with the provided scripts.

* test_base.sh - tests every request in a scenario where every service should be working (no search tests included here)
* test_no_auth.sh - will stop the keycloak service and test the authentication requests
* test_search.sh - test the search service and available results
* test_no_search.sh - will stop the search service and test the available search feature and other requests

