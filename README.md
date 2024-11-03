Summary
=======
This repo is a practice project for making a URL shortener. The design is based on the book System Design Interview - Chapter 8: Design A URL Shortener.

Usage
=====
Three applications have to be run for this URL shortener web application to operate.

1. **Dash app**  
This is the frontend of this web application, offering graphical user interface for users to generate shortened URLs.

2. **FastAPI endpoint**  
This is a RESTful API behind the scene that handles users requests to shorten a long URL or to visit the shortened URLs and be redirected to the corresponding long URLs.

3. **Redis cache**  
This is a RAM-based cache for storing recently accessed data. It runs within a Docker container using official Docker image [redis/redis-stack](https://hub.docker.com/r/redis/redis-stack).

Design
======
This URL shortener is a REST API that serves two requests:

1. **URL shortening**:  
When users want to shorten a URL, they send an HTTP POST request to the API, whhich contains one parameter, the long URL to be shortened. The API then returns a shortened URL, which has a domain of the API server and a path that is a unique ID for the input URL. 

For example: input_url = "https://google.com", output_url = "https://localhost/da1zH12R".

2. **Redirecting**:  
When anyone attempts to access any shortened URL with an HTTP GET request, the server changes the URL to the long URL stored in the server's database with 302 redirect status code.

Frameworks
==========
- API Endpoints - FastAPI
- Cache - Redis
- Database - SQLite

