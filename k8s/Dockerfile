FROM python:3.6

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN mkdir -p /app

COPY /app.py/ /app
COPY /requirements.txt/ /app
RUN pip3 install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

# For local testing
EXPOSE 8081
CMD ["python", "app.py"]
