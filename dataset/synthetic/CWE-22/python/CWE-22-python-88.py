import os
import tempfile

notes_root = os.path.join(tempfile.gettempdir(), "notes")


class NoteViewer:

    def list_notes(self):
        return os.listdir(notes_root)

    def open_note(self, name):
        file_path = os.path.join(notes_root, name)

        with open(file_path, "r", encoding="utf-8") as fh:
            return fh.read()


def main():
    viewer = NoteViewer()

    available = viewer.list_notes()
    print("notes:", available)

    choice = input("note: ").strip()
    if choice not in available:
        raise ValueError("invalid note")

    print(viewer.open_note(choice)[:60])


if __name__ == "__main__":
    main()