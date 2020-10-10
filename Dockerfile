FROM python:3.8.5-slim-buster

COPY entrypoint.sh /entrypoint.sh

# install curl; skipcq: DOK-DL3008
RUN apt-get update && apt-get install --no-install-recommends -y curl git && apt-get clean && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Install misspell cli binary
RUN curl -L -o ./install-misspell.sh https://git.io/misspell \
    && sh ./install-misspell.sh

ENTRYPOINT ["/entrypoint.sh"]
