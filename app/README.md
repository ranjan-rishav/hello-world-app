# Overview
A simple Helloworld Python application
* Uses Flask for API development
* Uses Pytest for testing APIs
* Uses Gunicorn for Application server
---
## Contents
- Dockerfile: 
    1. Uses centos 8 as base image
    2. Installs relevant packages
    3. Fetches app distribution package from target
    4. Installs app
    5. Starts app server on port 8080
- src:
    1. Contains App logic
    2. Contains unit tests
- setup.py:
    1. Used for packaging App
    2. Used for managing dependencies
    3. Used for version control
