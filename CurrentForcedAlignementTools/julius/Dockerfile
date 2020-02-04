FROM debian

RUN apt-get update \
    && apt-get install -y \
    curl \
    unzip

WORKDIR /julius
COPY install-julius.sh  editted-dnn.jconf ./
# RUN ./install-julius.sh