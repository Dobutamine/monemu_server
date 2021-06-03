FROM python:3.7

RUN pip install fastapi uvicorn aiofiles

EXPOSE 2340

COPY ./app /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]