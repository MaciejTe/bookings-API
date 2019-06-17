<!---
#######################################
## Simple Bookings REST API
##
## Format: markdown (md)
## Latest versions should be placed as first
##
## Notation: 00.01.02
##      - 00: stable released version
##      - 01: new features
##      - 02: bug fixes and small changes 
##
## Updating schema (mandatory):
##      <empty_line>
##      <version> (dd/mm/rrrr)
##      ----------------------
##      * <item>
##      * <item>
##      <empty_line>
##
## Useful tutorial: https://en.support.wordpress.com/markdown-quick-reference/
##
#######################################
-->
00.05.10 (17/06/2019)
---------------------
Implemented simple version of SSL
   - certificates are generated on the fly (ad-hoc option)
   - black used to reformat project
   - pyOpenSSL added to requirements file
   
00.05.00 (17/06/2019)
---------------------
Implemented /slots endpoint
   - added /slots endpoint
   - added cron job which generates slots every day
   - added tests for /slots enpoint
   
00.04.00 (14/04/2019)
---------------------
Implemented CRUD operations for /bookings endpoint
   - added tests for /bookings enpoint
   - upgraded Jinja2 to version 2.10.1 

00.03.00 (28/03/2019)
---------------------
Implemented CRUD operations for /users endpoint
   - added tests for /users enpoint
   - added new CLI command for code coverage test: flask coverage 
   - pytest-coverage plugin added to requirements.txt
    
    
00.02.00 (19/03/2019)
---------------------
Implemented CRUD operations for /resources endpoint
   - added test for resource enpoint

00.01.00 (16/03/2019)
---------------------
Implemented CRUD operations for /resources endpoint
   - used jsonschema to validate JSONs 
   - added draft version of libs/ package

00.00.03 (20/01/2019)
---------------------
Removed most of the code from \_\_init__.py's
   - added simple test example based on pytest and flask-testing

00.00.02 (04/11/2018)
---------------------
Improved and simplified some imports
   - added build_image section to Makefile
   - moved db object to src/\__init\__.py
   - added src/logger.py
   - added config.py with all Flask env vars

00.00.01 (04/11/2018)
---------------------
* Added core functionality based on Flask microframework:
    - database tables created with SQLAlchemy ORM
    - Flask CLI additional commands: initdb, dropdb
    - sample Dockerfile for development purposes
    - added Makefile with most common operations
    - sample resources API endpoint


00.00.00 (21/10/2018)
---------------------
* Created repository and associated files: LICENSE, README.md, .gitignore
