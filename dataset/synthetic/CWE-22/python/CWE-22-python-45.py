import os

media_root = "/srv/media/library"


def fetch_media(ref):
    file_ref = ref + ".mp3"
    path = os.path.join(media_root, file_ref)

    with open(path, "rb") as src:
        return src.read()


def run_player():
    track = input("track id: ").strip()
    data = fetch_media(track)
    print("loaded bytes:", len(data))


if __name__ == "__main__":
    run_player()