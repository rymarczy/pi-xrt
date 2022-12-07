# 93 XRT Pi Player
This project is meant to turn a raspberry pi into a mini radio station the plays nothing but the 93 XRT radio station.

## Requirements
This has been tested on a raspberry pi running debian. `docker`, `docker-compose` and `pulseaduio` are required to be installed on the host system.

```
sudo apt install docker docker-compose pulseaudio
```

## Operation
The most complicated part of this project is getting the audio from the docker container to play on the host system. 

This is achieved by basically passing the pulseaudio server from the host system into to the container.

This requires the user inside of the docker container to have the same `UID` as the user launching the container on the host system. 

The `UID` is passed into the container using the `.env` file. The required value can be foudn by running `id -u` on the host system and upating the `.env` file:

```
# update with value from running: id -u
UID=1000
```

## Startup

Once the `.env` file has been updated with the neccessary user id, launch the container:

```
docker-compose up -d
```

`-d` flag launches container in background

## Issues

I've run into a few issues on host system reboots. The host computer must start `pulseaudio` automatically, or the container will not be able to pass audio through.

On debian, it also seems like there could be a bit of race condtion between the `docker` daemon starting and `pulseaudio`.

Adding the following to your `docker` `systemd` configuration seems to fix this:
```
ConditionPathExists=/run/user/1000/pulse/native
```
the `1000` above being your `UID` in the `.env` file.