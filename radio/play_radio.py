from urllib.request import urlopen
import http.client as httplib
import subprocess
import time
import os

PWD = os.path.dirname(os.path.abspath(__file__))

def internet_available() -> bool:
    """
    check if internet is available by getting "HEAD" from google.com
    """
    conn = httplib.HTTPSConnection("google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception as _:
        return False
    finally:
        conn.close()


def get_radio_url() -> str:
    """
    get radio URL from static file, default to hard code is can't get from URL
    """
    try:
        with urlopen("https://ryanrymarczyk.com/radio.txt") as response:
            stream_url = response.read().decode().strip()
        return stream_url
    except Exception as _:
        pass

    return "https://live.amperwave.net/manifest/audacy-wxrtfmaac-hlsc.m3u8"


def start_player_process(stream_url: str) -> subprocess.Popen:
    stream_command = [
        "mplayer",
        "-cache",
        "8192",
        "-cache-min",
        "80",
        stream_url,
    ]
    return (
        subprocess.Popen(
            stream_command, 
            stdout=subprocess.DEVNULL, 
            stderr=subprocess.STDOUT
        )
    )


def play_no_internet() -> None:
    no_internet_file = os.path.join(PWD,"no_internet.flac")
    no_internet_cmd = [
        "mplayer",
        "-loop",
        "5",
        no_internet_file
    ]
    subprocess.run(
        no_internet_cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )


def main() -> None:
    """
    this runs radio player in loop with period checks to make sure 
    that internet is still connected and process is running
    """

    # restart player process after this many seconds, no matter what
    restart_duration_seconds = 60 * 60 * 13

    while True:
        # Check if internet connection is available
        # if is not, wait and retry in some seconds
        if internet_available() is False:
            play_no_internet()
            continue

        stream_url = get_radio_url()
        player_process = start_player_process(stream_url=stream_url)
        player_process_start_time = time.monotonic()

        # check if internet is still available and player is playing every 
        # so many seconds
        while True:
            if internet_available() is False:
                break

            if player_process.poll() is not None:
                break

            # periodocially restart player process
            current_duration = time.monotonic() - player_process_start_time
            if  current_duration > restart_duration_seconds:
                break

            time.sleep(15)

        player_process.kill()


if __name__ == "__main__":
    main()
