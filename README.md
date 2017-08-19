# uvaTextbookExchange

##General Description:
- Uva Textbook Exchange is an online applicaiton built using Django Framework
- It is a website that allows UVA students to both buy and sell thier textbooks (online marketplace)
- The highlights of this project is that it is completely built with the purpose to scale
- The application is based on a Microservices architecture and utilizes docker 
- Technologies used:
  - Django Framework
  - Docker
  - Continuous Integration (Selenium and Travis CI)
  - Haproxy for load-balancing
  - Spark (reccomendation engine for users)
  - Kafka
  - Elasticsearch

## Project 7
- Project 7 should work as expected. 
- After you run docker-compose up, please go to the website and view some of the listings using multiple accounts
- You can then run ./spark.sh to start the spark job that will run every 3 minutes. 
- The recommendation service needs at least three users to view an item before it will produce output and add it to table
- The recommendation is in a table format underneath each item listing


# Project 6:
- For this project, we completed the three required tasks: selenium, travis ci, and load blancing and in addition hosted our applications to Digital Ocean
- Travis CI output is included in our email to you
- The Digital ocean hosted application can be viewed at : http://107.170.22.151:8000/ (this only has the code for project 6 not 7)
- Selenium Instructions:
  - Our Selenium tests run completley separate from docker, they run locally on our models django application
  - Integration Testing with Selenium
    - We have two verions of our docker-compose file: docker-compose.yml and docker-compose.selenium.yml
    - In order to run a test, copy the contents of docker-compose.selenium.yml and replace the contents of the docker-compose.yml with that code 
    - To run a test simply run the command docker-compose run web1 (only creates containers necessary to allow web1 container to run the tests)
    - Inside web/frontend/tests.py you can only run a single test method that begins "test_load" because they would conflict with eachother if run at the same time
    - Therefore uncomment only one "test_load" test per run of docker-compose run web1, otherwise tests will unecessarily fail

-Haproxy load-balancing
  There is a haproxy docker container specified partially in the docker-compose file, but built from specifications in haproxy/Dockerfile as according to the config found at haproxy/haproxy.cfg. 
  It is facing port 8000, and directs incoming requests in a roundrobin fashion to either the web1 or web2 containers, now at ports 8003 and 8004 respectively. Evidence of this happening can be found in the haproxy screenshot in the screenshots folder, notice how at the bottom we repeated an action for which we have the server print out the response object, and the request was taken care of first by web2 and then by web1. (That action is logging in in case you want to test that out yourself.)
