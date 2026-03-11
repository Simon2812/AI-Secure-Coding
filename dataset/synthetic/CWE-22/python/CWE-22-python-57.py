import os
import tarfile


class ExtractionManager:

    def __init__(self, destination):
        self.destination = destination

    def unpack_one(self, archive_name, member_name):
        archive_path = os.path.join(os.getcwd(), archive_name)

        with tarfile.open(archive_path, "r") as bundle:
            member = bundle.extractfile(member_name)
            if member is None:
                raise ValueError("missing archive member")

            out_path = os.path.join(self.destination, member_name)
            with open(out_path, "wb") as sink:
                sink.write(member.read())


def main():
    target_dir = os.environ.get("RESTORE_TO", os.path.join(os.getcwd(), "restored"))

    manager = ExtractionManager(target_dir)
    archive = input("archive: ").strip()
    entry = input("member: ").strip()

    manager.unpack_one(archive, entry)


if __name__ == "__main__":
    main()