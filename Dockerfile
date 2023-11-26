FROM python:3.11

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver

EXPOSE 5000

ENV NAME World

CMD ["python", "app.py"]
