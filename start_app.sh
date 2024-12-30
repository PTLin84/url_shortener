# Start redis server (using official docker image)
docker run -p 6379:6379 -p 8001:8001 --name redis-stack redis/redis-stack:latest

# Start fastapi endpoint
fastapi run app/main.py &

# Start dash app (web UI)
# Demo with python development server, for production use WSGI server, e.g., gunicorn
python app/app.py