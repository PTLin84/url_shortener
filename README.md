This repo is a practice project for making a URL shortener. The design is based on the book System Design Interview - Chapter 8: Design A URL Shortener.

Usage
=====
To be udpated.

Design
======
This URL shortener is a REST API that serves two requests:

1. URL shortening:  
When users want to shorten a URL, they send an HTTP POST request to the API, whhich contains one parameter, the long URL to be shortened. The API then returns a shortened URL, which has a domain of the API server and a path that is a unique ID for the input URL. For example: input_url = "https://google.com", output_url = "https://localhost/da1zH12R".

2. Redirecting:
When anyone attempts to access any shortened URL with an HTTP GET request, the server changes the URL to the long URL stored in the server's database with 302 redirect status code.

Frameworks
==========
API Endpoints - FastAPI
Cache - Redis
Database - SQLite

