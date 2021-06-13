FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Copy app code to container
COPY src/app /app/app
# Copy requirements.txt to the container
COPY requirements.txt requirements.txt
# Install requirements
RUN pip install -r requirements.txt
# Copy ENV file
COPY docker/.env.docker .env
# Start the server
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080" ]