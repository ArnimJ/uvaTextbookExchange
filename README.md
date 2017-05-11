# uvaTextbookExchange

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
  - Steps to run Selenium:
    - Install Selenium:`pip install selenium`
    - Enter models project: `cd models`
    - Run test: `python manage.py test marketplace.tests.MySeleniumTests.test_name_here` where test_name_here is the name of a test from the set of tests under the MySelenium Tests class

Haproxy load-balancing
There is a haproxy docker container specified partially in the docker-compose file, but built from specifications in haproxy/Dockerfile as according to the config found at haproxy/haproxy.cfg. 
It is facing port 8000, and directs incoming requests in a roundrobin fashion to either the web1 or web2 containers, now at ports 8003 and 8004 respectively. Evidence of this happening can be found in the haproxy screenshot in the screenshots folder, notice how at the bottom we repeated an action for which we have the server print out the response object, and the request was taken care of first by web2 and then by web1. (That action is logging in in case you want to test that out yourself.)
