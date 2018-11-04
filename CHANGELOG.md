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
