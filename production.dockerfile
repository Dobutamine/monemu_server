# build stage -> shuts down after building the files
FROM python:3.7
RUN pip install fastapi uvicorn[standard] aiofiles
COPY ./app /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

