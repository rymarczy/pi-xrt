FROM debian:11

RUN apt-get update \
 && apt-get install --yes \
 --no-install-recommends \
 --no-install-suggests \
 python3 \
 pulseaudio \
 ca-certificates \
 mplayer

COPY radio /radio/
WORKDIR /radio/

ENTRYPOINT ["python3", "play_radio.py"]
