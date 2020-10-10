FROM python:3.8.5-slim-buster

RUN groupadd --gid 5000 main \
    && useradd --home-dir /home/main --create-home --uid 5000 \
        --gid 5000 --shell /bin/sh --skel /dev/null main

COPY . /app
WORKDIR /app

# install curl; skipcq: DOK-DL3008
RUN apt-get update && apt-get install --no-install-recommends -y curl git && apt-get clean && rm -rf /var/lib/apt/lists/*
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# download the misspell cli binary
RUN curl -L -o ./install-misspell.sh https://git.io/misspell \
    && sh ./install-misspell.sh

RUN ["chmod", "777", "/app/main.py"]

USER main

CMD ["/app/main.py"]
