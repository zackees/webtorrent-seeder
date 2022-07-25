# FROM ubuntu:22.04
FROM python:3.10-bullseye

# Might be necessary.
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /app

# Long install of cyrpto and other dependencies.
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    npm \
    ca-certificates \
    curl \
    gnupg2 \
    software-properties-common \
    unzip \
    wget \
    zip \
    && rm -rf /var/lib/apt/lists/*

# Quick install of app and dependencies.
COPY . .
# Install all the dependencies as it's own layer.
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Expose the port and then launch the app.
EXPOSE 80

# RUN npm install -g http-server

# CMD ["uvicorn", "--host", "0.0.0.0", "--port", "80", "webtorrent_seeder.app:app"]
# CMD ["python", "-m", "http.server", "--directory", "www", "--bind", "0.0.0.0", "80"]
CMD ["/bin/sh", "demo.sh"]
# install npm http-server
# CMD ["/bin/sh", "http-server", "-p 80"]
