# FROM ubuntu:22.04
FROM python:3.10-slim-bullseye

# Might be necessary.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app

COPY . .

# Install all the dependencies as it's own layer.
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir  -r requirements.txt



# Expose the port and then launch the app.
EXPOSE 80

# CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "webtorrent_seeder.app:app"]
