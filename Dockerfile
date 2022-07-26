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

RUN npm install --location=global https://github.com/zackees/webtorrent-hybrid


# Expose the port and then launch the app.
EXPOSE 80

CMD ["/bin/sh", "demo.sh"]
