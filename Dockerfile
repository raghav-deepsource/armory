FROM python:3.8.5-slim-buster

COPY . /app
WORKDIR /app

# install curl; skipcq: DOK-DL3008
RUN apt-get update && apt-get install --no-install-recommends -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# download the misspell cli binary
RUN curl -L -o ./install-misspell.sh https://git.io/misspell \
    && sh ./install-misspell.sh
RUN ["chmod", "777", "/app/entrypoint.sh"]

ENTRYPOINT ["/app/entrypoint.sh"]
