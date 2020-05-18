FROM debian

RUN apt-get update \
    && apt-get install -y \
    curl \
    unzip

WORKDIR /aeneas
COPY install-aeneas.sh ./install-aeneas.sh
RUN ./install-aeneas.sh
WORKDIR /workdir