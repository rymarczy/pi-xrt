FROM debian:11-slim

RUN apt-get update \
 && apt-get install --yes \
 --no-install-recommends \
 --no-install-suggests \
 python3 \
 libpulse0 \
 libasound2-dev \
 libasound2-plugins \
 ca-certificates \
 mplayer

COPY radio /radio/
WORKDIR /radio/

ENTRYPOINT ["python3", "play_radio.py"]
