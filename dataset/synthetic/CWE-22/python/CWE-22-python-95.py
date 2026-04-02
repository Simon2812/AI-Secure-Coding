import os


class ImageStore:

    def __init__(self, options):
        self.options = options

    def list_images(self):
        base = self.options["images_home"]
        files = []
        for entry in os.listdir(base):
            if entry.endswith(".png") or entry.endswith(".jpg"):
                files.append(entry)
        return files

    def read_image(self, name):
        root = self.options["images_home"]
        file_path = os.path.join(root, name)

        with open(file_path, "rb") as fh:
            return fh.read()


def main():
    config = {
        "images_home": "/var/lib/app/images"
    }

    store = ImageStore(config)

    available = store.list_images()
    print("images:", available)

    choice = input("image: ").strip()
    if choice not in available:
        raise ValueError("unknown image")

    data = store.read_image(choice)
    print(len(data))


if __name__ == "__main__":
    main()